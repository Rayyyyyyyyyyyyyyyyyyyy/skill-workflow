"""SQLite reference of durable jobs/sessions. NOT production authorization, sandboxing or QA.

Python stdlib only. Demonstrates transactional job state, attempts, fencing, checkpoints,
and cross-repository dependencies. Replace SQLite with a properly secured Postgres
service plus authenticated APIs, short-lived credentials, and a real worker supervisor.
"""
from __future__ import annotations
import json
import sqlite3
import time
import uuid
from pathlib import Path


class StateError(RuntimeError):
    pass


class StaleAttempt(StateError):
    pass


class DurableStore:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(str(path), timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS agents (
            agent_id TEXT PRIMARY KEY, role_id TEXT NOT NULL, profile_version TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY, workflow_id TEXT NOT NULL, required_role TEXT NOT NULL,
            approved_brief_ref TEXT NOT NULL, repo_id TEXT NOT NULL,
            base_sha TEXT NOT NULL, allowed_paths_json TEXT NOT NULL,
            state TEXT NOT NULL DEFAULT 'READY',
            current_attempt_id TEXT, fence_generation INTEGER NOT NULL DEFAULT 0,
            checkpoint_ref TEXT, checkpoint_progress_json TEXT,
            result_ref TEXT, qa_manifest_ref TEXT, updated_at REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dependencies (
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            needs_job_id TEXT NOT NULL REFERENCES jobs(job_id),
            PRIMARY KEY(job_id, needs_job_id), CHECK(job_id != needs_job_id)
        );
        CREATE TABLE IF NOT EXISTS attempts (
            attempt_id TEXT PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(job_id),
            fence_generation INTEGER NOT NULL, agent_id TEXT NOT NULL REFERENCES agents(agent_id),
            session_id TEXT NOT NULL, state TEXT NOT NULL, lease_until REAL NOT NULL,
            worktree_ref TEXT NOT NULL, UNIQUE(job_id, fence_generation)
        );
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY, agent_id TEXT NOT NULL REFERENCES agents(agent_id),
            attempt_id TEXT NOT NULL REFERENCES attempts(attempt_id),
            created_at REAL NOT NULL, closed_at REAL
        );
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id TEXT NOT NULL REFERENCES jobs(job_id),
            event_type TEXT NOT NULL, attempt_id TEXT, payload_json TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        ''')
        self.db.commit()

    def close(self):
        self.db.close()

    def _tx(self, action):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            result = action()
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    def _event(self, job_id, typ, attempt_id=None, data=None):
        self.db.execute("INSERT INTO events(job_id,event_type,attempt_id,payload_json,created_at) VALUES (?,?,?,?,?)",
                        (job_id, typ, attempt_id, json.dumps(data or {}, sort_keys=True), time.time()))

    def register_agent(self, agent_id, role_id, profile_version="pinned-v1"):
        self.db.execute("INSERT INTO agents VALUES(?,?,?)", (agent_id, role_id, profile_version))
        self.db.commit()

    def create_job(self, job_id, workflow_id, required_role, approved_brief_ref,
                   repo_id, base_sha, allowed_paths, needs=()):
        if not approved_brief_ref or not repo_id or not base_sha or not allowed_paths:
            raise StateError("required job provenance missing")
        def action():
            for dep in needs:
                row = self.db.execute("SELECT workflow_id FROM jobs WHERE job_id=?", (dep,)).fetchone()
                if row is None or row['workflow_id'] != workflow_id:
                    raise StateError("dependency missing or outside workflow")
            self.db.execute("""INSERT INTO jobs(job_id,workflow_id,required_role,approved_brief_ref,repo_id,base_sha,allowed_paths_json,updated_at)
                               VALUES (?,?,?,?,?,?,?,?)""",
                            (job_id, workflow_id, required_role, approved_brief_ref, repo_id, base_sha,
                             json.dumps(allowed_paths), time.time()))
            self.db.executemany("INSERT INTO dependencies(job_id,needs_job_id) VALUES (?,?)", ((job_id,d) for d in needs))
            self._event(job_id, 'JOB_CREATED', data={'needs': list(needs), 'repo_id': repo_id})
        self._tx(action)

    def _require_active(self, attempt_id, fence, session_id, *, allowed_state=('RUNNING',)):
        row = self.db.execute("""SELECT j.job_id, j.state, j.current_attempt_id, j.fence_generation,
                           a.state AS attempt_state, a.lease_until, a.session_id, s.closed_at
                           FROM attempts a JOIN jobs j ON j.job_id=a.job_id
                           JOIN sessions s ON s.session_id=a.session_id
                           WHERE a.attempt_id=?""", (attempt_id,)).fetchone()
        if (not row or row['current_attempt_id'] != attempt_id or
                row['fence_generation'] != fence or row['session_id'] != session_id or
                row['closed_at'] is not None or row['state'] not in allowed_state or
                row['attempt_state'] != 'RUNNING' or row['lease_until'] <= time.time()):
            raise StaleAttempt("attempt revoked, expired, superseded, or session closed")
        return row['job_id']

    def claim(self, job_id, agent_id, lease_seconds=120):
        if lease_seconds <= 0:
            raise StateError("positive lease required")
        def action():
            j = self.db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            a = self.db.execute("SELECT * FROM agents WHERE agent_id=?", (agent_id,)).fetchone()
            if j is None or a is None or a['role_id'] != j['required_role']:
                raise StateError("unknown job/agent or wrong role")
            if j['state'] != 'READY':
                raise StateError("job not claimable")
            open_deps = self.db.execute("""SELECT 1 FROM dependencies d JOIN jobs j ON j.job_id=d.needs_job_id
                                       WHERE d.job_id=? AND j.state!='DONE' LIMIT 1""", (job_id,)).fetchone()
            if open_deps:
                raise StateError("blocked on dependencies")
            aid, sid = uuid.uuid4().hex, uuid.uuid4().hex
            fence = j['fence_generation'] + 1
            # Logical reference; a real workspace provisioner creates and verifies the worktree.
            worktree_ref = f"workspace://{job_id}/{aid}"
            expiry = time.time() + lease_seconds
            self.db.execute("INSERT INTO attempts VALUES(?,?,?,?,?,?,?,?)",
                            (aid, job_id, fence, agent_id, sid, 'RUNNING', expiry, worktree_ref))
            self.db.execute("INSERT INTO sessions VALUES(?,?,?,?,NULL)",
                            (sid, agent_id, aid, time.time()))
            self.db.execute("""UPDATE jobs SET state='RUNNING',current_attempt_id=?,fence_generation=?,updated_at=?
                               WHERE job_id=?""", (aid, fence, time.time(), job_id))
            self._event(job_id, 'ATTEMPT_CLAIMED', aid, {'fence': fence, 'session_id': sid})
            return {'job_id': job_id, 'attempt_id': aid, 'session_id': sid,
                    'agent_id': agent_id, 'fence_generation': fence, 'worktree_ref': worktree_ref,
                    'repo_id': j['repo_id'], 'base_sha': j['base_sha'],
                    'checkpoint_ref': j['checkpoint_ref'],
                    'checkpoint_progress': json.loads(j['checkpoint_progress_json']) if j['checkpoint_progress_json'] else None}
        return self._tx(action)

    def checkpoint(self, attempt_id, fence, session_id, artifact_ref, progress):
        if not artifact_ref or not isinstance(progress, dict):
            raise StateError("checkpoint must be artifact reference + structured progress")
        def action():
            job_id = self._require_active(attempt_id, fence, session_id)
            self.db.execute("""UPDATE jobs SET checkpoint_ref=?, checkpoint_progress_json=?, updated_at=?
                               WHERE job_id=?""", (artifact_ref, json.dumps(progress), time.time(), job_id))
            self._event(job_id, 'CHECKPOINT_SAVED', attempt_id, {'ref': artifact_ref, 'progress': progress})
        self._tx(action)

    def suspend(self, attempt_id, fence, session_id):
        """Voluntary handoff. Real runner MUST stop/revoke external write capability first."""
        def action():
            job_id = self._require_active(attempt_id, fence, session_id)
            r = self.db.execute("SELECT checkpoint_ref FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            if not r['checkpoint_ref']:
                raise StateError("checkpoint required before suspension")
            self.db.execute("UPDATE attempts SET state='SUPERSEDED' WHERE attempt_id=?", (attempt_id,))
            self.db.execute("UPDATE sessions SET closed_at=? WHERE session_id=?", (time.time(), session_id))
            self.db.execute("UPDATE jobs SET state='READY', current_attempt_id=NULL, updated_at=? WHERE job_id=?",
                            (time.time(), job_id))
            self._event(job_id, 'HANDOFF_SUSPENDED', attempt_id)
        self._tx(action)

    def submit(self, attempt_id, fence, session_id, result_ref):
        if not result_ref:
            raise StateError("result reference required")
        def action():
            job_id = self._require_active(attempt_id, fence, session_id)
            self.db.execute("UPDATE jobs SET state='AWAITING_QA',result_ref=?,updated_at=? WHERE job_id=?",
                            (result_ref, time.time(), job_id))
            self.db.execute("UPDATE attempts SET state='SUBMITTED' WHERE attempt_id=?", (attempt_id,))
            self.db.execute("UPDATE sessions SET closed_at=? WHERE session_id=?", (time.time(), session_id))
            self._event(job_id, 'RESULT_SUBMITTED', attempt_id, {'result_ref': result_ref})
        self._tx(action)

    def qa_accept(self, job_id, attempt_id, fence, evidence_ref):
        """Simulated QA acceptance only. Real B11 must verify SHA + signed evidence."""
        if not evidence_ref:
            raise StateError("evidence required")
        def action():
            j = self.db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            if (not j or j['state']!='AWAITING_QA' or j['current_attempt_id']!=attempt_id or
                    j['fence_generation']!=fence):
                raise StaleAttempt("QA for wrong attempt or job state")
            self.db.execute("UPDATE jobs SET state='DONE',qa_manifest_ref=?,updated_at=? WHERE job_id=?",
                            (evidence_ref, time.time(), job_id))
            self._event(job_id, 'QA_ACCEPTED', attempt_id, {'evidence_ref': evidence_ref})
        self._tx(action)

    def reap_expired(self):
        """Revoke leases in DB; real B07/B26 must quarantine/terminate worker before re-claim."""
        def action():
            rows = self.db.execute("""SELECT j.job_id,a.attempt_id,a.session_id FROM jobs j JOIN attempts a
                                   ON a.attempt_id=j.current_attempt_id
                                   WHERE j.state='RUNNING' AND a.lease_until<=?""", (time.time(),)).fetchall()
            for row in rows:
                self.db.execute("UPDATE attempts SET state='EXPIRED' WHERE attempt_id=?", (row['attempt_id'],))
                self.db.execute("UPDATE sessions SET closed_at=? WHERE session_id=?", (time.time(), row['session_id']))
                # QUARANTINED pending external termination; never immediately lease a second writer.
                self.db.execute("UPDATE jobs SET state='QUARANTINED', current_attempt_id=NULL,updated_at=? WHERE job_id=?",
                                (time.time(),row['job_id']))
                self._event(row['job_id'],'ATTEMPT_EXPIRED',row['attempt_id'])
            return len(rows)
        return self._tx(action)

    def certify_stopped(self, job_id, stopped_attempt_id):
        """Reference only. Caller assertion NOT verified; production must trust supervisor attestation."""
        def action():
            j = self.db.execute("SELECT * FROM jobs WHERE job_id=?", (job_id,)).fetchone()
            a = self.db.execute("SELECT * FROM attempts WHERE attempt_id=?",(stopped_attempt_id,)).fetchone()
            if not j or not a or a['job_id']!=job_id or a['state']!='EXPIRED' or j['state']!='QUARANTINED':
                raise StateError("not awaiting confirmed stop")
            self.db.execute("UPDATE jobs SET state='READY',updated_at=? WHERE job_id=?",(time.time(),job_id))
            self._event(job_id,'STOP_CERTIFIED',stopped_attempt_id)
        self._tx(action)

    def state(self, job_id):
        row = self.db.execute("SELECT * FROM jobs WHERE job_id=?",(job_id,)).fetchone()
        return dict(row) if row else None

    def event_types(self, job_id):
        return [r['event_type'] for r in self.db.execute("SELECT event_type FROM events WHERE job_id=? ORDER BY event_id",(job_id,))]
