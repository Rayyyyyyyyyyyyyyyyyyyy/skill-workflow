# Historical test fixture only; never imported by production.
# Source: private baseline c670ae2dc345f3e2d870b60b57bf6840eee53c7c:workbench.py
# Original source SHA-256: ecec96a7f6d49960882e71dd551701cf5dbe92c6f24b4990262ed884031fda5a
# --- original source follows ---
"""Trusted local workflow control. Codex supplies authors and independent reviewers.

This module controls its own records, not OS permissions or external side effects.
Only the host controller should call mutation commands; actor IDs are host receipts,
not authentication credentials. Python 3.11+, standard library only.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import tomllib
import uuid


class WorkflowError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise WorkflowError(message)


def wire(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else wire(value).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


class Workbench:
    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).parent).resolve()

    def project(self, slug):
        require(isinstance(slug, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", slug), "invalid project ID")
        path = self.root / "projects" / slug
        require(not path.is_symlink() and not path.parent.is_symlink(), "symlink project rejected")
        return path

    def _db(self, slug):
        path = self.project(slug) / ".workflow" / "state.sqlite3"
        require(path.is_file() and not path.is_symlink() and not path.parent.is_symlink(), "project not found or unsafe state path")
        db = sqlite3.connect(path, timeout=10)
        db.execute("PRAGMA foreign_keys=ON")
        return db

    @contextmanager
    def _edit(self, slug, event):
        db = self._db(slug)
        try:
            db.execute("BEGIN IMMEDIATE")
            state = json.loads(db.execute("SELECT data FROM project WHERE id=1").fetchone()[0])
            yield state
            state["updated_at"] = now()
            db.execute("UPDATE project SET data=? WHERE id=1", (wire(state),))
            db.execute("INSERT INTO events(at,kind,state_digest) VALUES(?,?,?)", (now(), event, digest(state)))
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def _blob(self, slug, data):
        sha = digest(data)
        folder = self.project(slug) / ".workflow" / "blobs"
        folder.mkdir(exist_ok=True)
        require(not folder.is_symlink(), "unsafe blob store")
        path = folder / sha
        if path.exists():
            require(not path.is_symlink() and digest(path.read_bytes()) == sha, "corrupt blob")
        else:
            try:
                with path.open("xb") as target:
                    target.write(data)
                path.chmod(0o444)
            except FileExistsError:
                require(digest(path.read_bytes()) == sha, "corrupt blob")
        return sha

    def _read_blob(self, slug, sha):
        require(isinstance(sha, str) and re.fullmatch(r"[a-f0-9]{64}", sha), "invalid digest")
        path = self.project(slug) / ".workflow" / "blobs" / sha
        require(path.is_file() and not path.is_symlink(), "missing blob")
        data = path.read_bytes()
        require(digest(data) == sha, "blob digest mismatch")
        return data

    def _snapshot(self, slug, source):
        require(isinstance(source, dict) and nonempty(source.get("path")), "source path required")
        path = Path(source["path"]).expanduser()
        if not path.is_absolute():
            path = self.root / path
        require(path.is_file() and not path.is_symlink(), f"method source missing: {path}")
        data = path.read_bytes()
        fmt = source.get("format", "text")
        if fmt == "toml":
            require(nonempty(tomllib.loads(data.decode()).get("developer_instructions")), "role instructions missing")
        else:
            require(fmt == "text" and nonempty(data.decode()), "invalid method source")
        return {"path": str(path), "sha256": self._blob(slug, data), "format": fmt}

    def _instructions(self, slug, source):
        text = self._read_blob(slug, source["sha256"]).decode()
        return tomllib.loads(text)["developer_instructions"] if source["format"] == "toml" else text

    def _workspace(self, slug, state):
        raw = state.get("plan", {}).get("workspace")
        return self.root if raw == "." else self.project(slug) / "workspace"

    def _file(self, slug, state, relative):
        require(nonempty(relative) and "\\" not in relative, "invalid file path")
        part = Path(relative)
        require(not part.is_absolute() and all(x not in ("", ".", "..") for x in relative.split("/")), "path must be a clean relative file path")
        require(".workflow" not in part.parts and ".git" not in part.parts, "control files are not deliverables")
        base = self._workspace(slug, state)
        cursor = base
        require(not base.is_symlink(), "symlink workspace rejected")
        for item in part.parts:
            cursor = cursor / item
            require(not cursor.is_symlink(), "symlink artifact rejected")
        require(cursor.resolve().is_relative_to(base.resolve()) and cursor.is_file(), f"file missing or outside workspace: {relative}")
        if state.get("plan", {}).get("workspace") == ".":
            allowed = state["plan"]["allowed_paths"]
            require(any(relative == p or relative.startswith(p.rstrip("/") + "/") for p in allowed), "file outside approved paths")
        return cursor

    def _seal_files(self, slug, state, files):
        require(isinstance(files, list) and files and all(nonempty(f) for f in files) and len(files) == len(set(files)), "nonempty unique file list required")
        return {path: self._blob(slug, self._file(slug, state, path).read_bytes()) for path in files}

    def _task(self, state, task_id):
        require(task_id in state.get("tasks", {}), "unknown task")
        return state["tasks"][task_id]

    def _active(self, state, task_id, attempt):
        task = self._task(state, task_id)
        require(state["state"] != "CANCELLED", "project cancelled")
        require(task["state"] == "RUNNING" and task.get("attempt_id") == attempt, "stale or inactive attempt")
        return task

    def _summarize(self, state):
        if state["state"] == "CANCELLED":
            return
        tasks = list(state.get("tasks", {}).values())
        if not tasks:
            return
        if all(t["state"] == "DONE" for t in tasks):
            state["state"] = "DONE" if state["plan"]["scope"] == "deliver" else "WAITING"
            state["reason"] = None if state["state"] == "DONE" else "DELIVERY_PLAN_REQUIRED"
        elif any(t["state"] == "RUNNING" for t in tasks):
            state["state"] = "RUNNING"
        elif any(t["state"] == "AWAITING_REVIEW" for t in tasks):
            state["state"] = "AWAITING_REVIEW"
        elif any(t["state"] == "WAITING" for t in tasks):
            state["state"] = "WAITING"
        else:
            state["state"] = "READY"

    def new(self, slug, idea):
        require(nonempty(idea), "original idea required")
        project = self.project(slug)
        require(not project.exists(), "project already exists; use status to resume")
        project.mkdir(parents=True)
        (project / "workspace").mkdir()
        (project / ".workflow").mkdir()
        state = {"id": slug, "idea": idea, "state": "PLANNING", "created_at": now(), "tasks": {}, "history": []}
        db = sqlite3.connect(project / ".workflow" / "state.sqlite3")
        try:
            db.executescript("CREATE TABLE project(id INTEGER PRIMARY KEY CHECK(id=1),data TEXT NOT NULL); CREATE TABLE events(id INTEGER PRIMARY KEY,at TEXT NOT NULL,kind TEXT NOT NULL,state_digest TEXT NOT NULL);")
            db.execute("INSERT INTO project VALUES(1,?)", (wire(state),))
            db.execute("INSERT INTO events(at,kind,state_digest) VALUES(?,?,?)", (now(), "CREATE", digest(state)))
            db.commit()
        finally:
            db.close()
        (project / "PROJECT.md").write_text(f"# {slug}\n\n## 原始想法\n\n{idea}\n\n進度與接續：在集合根目錄執行 `python3 workbench.py status {slug}`。\n正式狀態與版本保存在 `.workflow/`；成果預設放 `workspace/`。\n", encoding="utf-8")
        return state

    def status(self, slug):
        db = self._db(slug)
        try:
            return json.loads(db.execute("SELECT data FROM project WHERE id=1").fetchone()[0])
        finally:
            db.close()

    def list(self):
        return [{"id": p.name, "state": self.status(p.name)["state"]} for p in sorted((self.root / "projects").glob("*")) if (p / ".workflow/state.sqlite3").is_file()]

    def plan(self, slug, plan):
        require(isinstance(plan, dict), "plan must be an object")
        candidate = json.loads(wire(plan))
        require(candidate.get("scope") in ("prepare", "deliver"), "scope must be prepare or deliver")
        routing = candidate.get("routing", {})
        require(isinstance(routing, dict), "routing must be an object")
        require(routing.get("maturity") in ("ready", "unclear", "needs-research", "needs-design") and nonempty(routing.get("reason")), "routing decision and reason required")
        require(isinstance(routing.get("missing_inputs"), list), "missing_inputs list required")
        require(candidate.get("operations", ["local"]) == ["local"], "external operations unsupported")
        limits = candidate.get("limits", {"max_rounds": 2, "review_retries": 2})
        require(isinstance(limits, dict), "limits must be an object")
        require(limits.get("max_rounds") == 2 and type(limits.get("review_retries")) is int and 0 <= limits["review_retries"] <= 2, "review limits must be bounded, at most two rounds/retries")
        limits.setdefault("max_attempts", 4)
        require(type(limits["max_attempts"]) is int and 1 <= limits["max_attempts"] <= 4, "at most four author attempts per task")
        candidate["limits"] = limits
        require(candidate.get("workspace") in (None, "."), "workspace must be project default or collection root")
        if candidate.get("workspace") == ".":
            paths = candidate.get("allowed_paths")
            require(isinstance(paths, list) and paths and all(nonempty(p) and not Path(p).is_absolute() and all(x not in ("", ".", "..", ".git", ".workflow") for x in p.rstrip("/").split("/")) for p in paths), "explicit clean allowed_paths required for root maintenance")
        requirements = candidate.get("requirements")
        require(isinstance(requirements, list) and requirements and all(isinstance(r, dict) and nonempty(r.get("id")) and nonempty(r.get("text")) for r in requirements), "requirements required")
        req_ids = {r["id"] for r in requirements}
        require(len(req_ids) == len(requirements), "duplicate requirement ID")
        entries = candidate.get("tasks")
        require(isinstance(entries, list) and 1 <= len(entries) <= 32 and all(isinstance(t, dict) for t in entries), "one to 32 fixed task objects required")
        ids = [t.get("id") for t in entries]
        require(all(nonempty(i) and re.fullmatch(r"[A-Za-z0-9_-]+", i) for i in ids) and len(set(ids)) == len(ids), "invalid or duplicate task ID")
        roles = json.loads((self.root / "library/roles.json").read_text())["roles"]
        with self._edit(slug, "PLAN") as state:
            old_tasks = list(state.get("tasks", {}).values())
            require(state["state"] not in ("CANCELLED", "DONE"), "terminal project cannot be replanned")
            require(state.get("plan_review_failures", 0) < 2, "plan review exhausted; goal alignment required")
            require(not old_tasks or all(t.get("generation", 0) == 0 for t in old_tasks) or (state["plan"]["scope"] == "prepare" and all(t["state"] == "DONE" for t in old_tasks)), "active/delivery contract cannot be replaced or reset")
            if state.get("plan"):
                state["history"].append({"plan": state["plan"], "tasks": state["tasks"], "plan_hash": state["plan_hash"]})
            bindings = {}
            covered = set()
            tasks = {}
            for original in entries:
                t = json.loads(wire(original))
                require(t.get("playbook") in ("clarify", "research", "design", "deliver"), "unknown author Playbook")
                path = self.root / "library/playbooks" / (t["playbook"] + ".json")
                playbook_bytes = path.read_bytes()
                playbook = json.loads(playbook_bytes)
                role = t.get("role")
                require(nonempty(role) and role in roles and role in playbook["roles"], "role incompatible with Playbook")
                require(isinstance(t.get("depends_on"), list) and all(nonempty(d) for d in t["depends_on"]) and len(t["depends_on"]) == len(set(t["depends_on"])) and all(d in ids and d != t["id"] for d in t["depends_on"]), "invalid dependencies")
                require(isinstance(t.get("requirement_ids"), list) and t["requirement_ids"] and all(nonempty(r) for r in t["requirement_ids"]) and set(t["requirement_ids"]) <= req_ids, "task requirements missing or unknown")
                acceptance = t.get("acceptance")
                require(isinstance(acceptance, list) and acceptance and all(isinstance(a, dict) for a in acceptance), "task acceptance objects required")
                for check in acceptance:
                    require(nonempty(check.get("id")) and not check["id"].startswith("PB-") and nonempty(check.get("description")) and nonempty(check.get("method")), "invalid acceptance")
                    require(isinstance(check.get("requirement_ids"), list) and check["requirement_ids"] and all(nonempty(r) for r in check["requirement_ids"]) and set(check["requirement_ids"]) <= set(t["requirement_ids"]), "acceptance requirement mapping invalid")
                    covered.update(check["requirement_ids"])
                require(len({a["id"] for a in acceptance}) == len(acceptance), "duplicate acceptance ID")
                for minimum in playbook["required_criteria"]:
                    acceptance.append({"id": f"PB-{t['id']}-{minimum['id']}", "requirement_ids": t["requirement_ids"], "description": minimum["description"], "method": minimum["method"]})
                t["acceptance"] = acceptance
                support = t.get("supporting_sources", [])
                require(isinstance(support, list), "supporting_sources must be explicit source descriptors")
                t["supporting_sources"] = [self._snapshot(slug, source) for source in support]
                role_ids = (role, "reviewer")
                for role_id in role_ids:
                    if role_id not in bindings:
                        profile = roles[role_id]
                        bindings[role_id] = {"role": self._snapshot(slug, profile["source"]), "skills": [self._snapshot(slug, source) for source in profile.get("skills", [])]}
                t["playbook_digest"] = self._blob(slug, playbook_bytes)
                t["state"] = "READY"
                t["generation"] = 0
                t["round"] = 0
                t["submissions"] = []
                tasks[t["id"]] = t
            require(covered == req_ids, "uncovered original requirement")
            visited, visiting = set(), set()

            def visit(task_id):
                require(task_id not in visiting, "dependency cycle")
                if task_id in visited:
                    return
                visiting.add(task_id)
                for dep in tasks[task_id]["depends_on"]:
                    visit(dep)
                visiting.remove(task_id)
                visited.add(task_id)

            for task_id in tasks:
                visit(task_id)
            policy = self._snapshot(slug, {"path": "runtime-reference/policies/P00-GROUNDED-ANSWER.md"})
            config = json.loads((self.root / "runtime-reference/config/global-policy.json").read_text())
            require(policy["sha256"] == config["required_policies"][0]["policy_sha256"], "P00 policy digest mismatch")
            review_contract = self._snapshot(slug, {"path": "library/playbooks/review.json"})
            candidate["bindings"] = bindings
            candidate["policy"] = policy
            candidate["review_contract"] = review_contract
            candidate["tasks"] = [{k: v for k, v in t.items() if k not in ("state", "generation", "round", "submissions")} for t in tasks.values()]
            candidate["planner"] = candidate.get("planner", "controller")
            require(nonempty(candidate["planner"]), "planner identity required")
            require(isinstance(candidate.get("contributors", []), list) and all(nonempty(a) for a in candidate.get("contributors", [])), "invalid plan contributors")
            state.update(plan=candidate, plan_hash=digest(candidate), tasks=tasks, plan_approval=None, state="WAITING" if routing["missing_inputs"] else "PLANNING", reason="INPUT_MISSING" if routing["missing_inputs"] else "PLAN_REVIEW_REQUIRED")
        return self.status(slug)

    def approve_plan(self, slug, report):
        require(isinstance(report, dict), "plan review must be an object")
        rejected = False
        with self._edit(slug, "PLAN_REVIEW") as state:
            require(state.get("plan") and report.get("plan_hash") == state["plan_hash"], "stale plan review")
            if state.get("plan_approval"):
                require(state["plan_approval"]["report"] == report, "plan review already fixed")
                return state
            require(not state["plan"]["routing"]["missing_inputs"], "critical input missing")
            plan_authors = [state["plan"]["planner"], *state["plan"].get("contributors", [])]
            require(nonempty(report.get("reviewer")) and report["reviewer"] not in plan_authors, "independent plan reviewer required")
            require(report.get("status") in ("PASS", "FAIL") and nonempty(report.get("reason")), "plan completeness verdict and reason required")
            evidence = self._seal_files(slug, state, [report.get("evidence")])
            reviews = state.setdefault("plan_reviews", [])
            if not any(entry["report"] == report for entry in reviews):
                reviews.append({"report": report, "evidence": evidence})
                if report["status"] == "FAIL":
                    state["plan_review_failures"] = state.get("plan_review_failures", 0) + 1
            if report["status"] == "FAIL":
                state.update(state="WAITING", reason="PLAN_ALIGNMENT_REQUIRED" if state.get("plan_review_failures", 0) >= 2 else "PLAN_REWORK_REQUIRED")
                rejected = True
            else:
                require(state.get("plan_review_failures", 0) < 2, "plan review exhausted; goal alignment required")
                state["plan_approval"] = {"report": report, "evidence": evidence}
                state.update(state="READY", reason=None)
        if rejected:
            raise WorkflowError("plan review failed; findings saved, no execution admitted")
        return self.status(slug)

    def _check_plan(self, slug, state):
        require(state["state"] != "CANCELLED" and state.get("plan_approval"), "approved plan required")
        require(digest(state["plan"]) == state["plan_hash"], "plan digest mismatch")
        for sha in state["plan_approval"]["evidence"].values():
            self._read_blob(slug, sha)
        for binding in state["plan"]["bindings"].values():
            for source in [binding["role"], *binding["skills"]]:
                self._read_blob(slug, source["sha256"])
        self._read_blob(slug, state["plan"]["policy"]["sha256"])
        self._read_blob(slug, state["plan"]["review_contract"]["sha256"])
        for task in state["tasks"].values():
            for source in task.get("supporting_sources", []):
                self._read_blob(slug, source["sha256"])

    def _packet(self, slug, state, task, purpose):
        binding = state["plan"]["bindings"]["reviewer" if purpose == "review" else task["role"]]
        return {"project_id": slug, "idea": state["idea"], "requirements": state["plan"]["requirements"], "plan_hash": state["plan_hash"], "task": task, "workspace": str(self._workspace(slug, state)), "policy": self._instructions(slug, state["plan"]["policy"]), "role_instructions": self._instructions(slug, binding["role"]), "skill_instructions": [self._instructions(slug, s) for s in binding["skills"]], "supporting_instructions": [{"source": s, "content": self._instructions(slug, s)} for s in task.get("supporting_sources", [])], "playbook": json.loads(self._read_blob(slug, task["playbook_digest"])), "review_playbook": json.loads(self._read_blob(slug, state["plan"]["review_contract"]["sha256"])), "blobs": str(self.project(slug) / ".workflow/blobs")}

    def dispatch(self, slug, task_id, actor, contributors=None):
        require(nonempty(actor), "host actor identity required")
        require(contributors is None or isinstance(contributors, list) and all(nonempty(a) for a in contributors), "invalid contributors")
        with self._edit(slug, "DISPATCH") as state:
            self._check_plan(slug, state)
            task = self._task(state, task_id)
            require(task["state"] == "READY" and task["round"] < 2, "task not dispatchable")
            require(task["generation"] < state["plan"]["limits"]["max_attempts"], "author attempts exhausted; preserve progress for decision")
            require(all(state["tasks"][d]["state"] == "DONE" for d in task["depends_on"]), "upstream not accepted")
            for dep in task["depends_on"]:
                for sha in state["tasks"][dep]["submission"]["files"].values():
                    self._read_blob(slug, sha)
            prior_authors = task.get("all_contributors", [])
            authors = sorted(set([*prior_authors, actor, *(contributors or [])]))
            require(all(nonempty(a) for a in authors), "invalid contributor identity")
            task.update(state="RUNNING", attempt_id=uuid.uuid4().hex, generation=task["generation"] + 1, actor=actor, contributors=authors, all_contributors=authors)
            task["inputs"] = {dep: state["tasks"][dep]["submission"] for dep in task["depends_on"]}
            task["contract_digest"] = digest({"plan": state["plan_hash"], "task": task_id, "playbook": task["playbook_digest"]})
            task["baseline_digest"] = digest(task["acceptance"])
            self._summarize(state)
            packet = self._packet(slug, state, task, "author")
        return {"attempt_id": task["attempt_id"], "contract_digest": task["contract_digest"], "baseline_digest": task["baseline_digest"], "packet": packet}

    def checkpoint(self, slug, task_id, attempt, files, note):
        require(nonempty(note), "checkpoint next action required")
        with self._edit(slug, "CHECKPOINT") as state:
            task = self._active(state, task_id, attempt)
            task["checkpoint"] = {"files": self._seal_files(slug, state, files), "note": note, "attempt_id": attempt, "at": now()}
        return self.status(slug)

    def pause(self, slug, task_id, attempt, note, stopped=False):
        require(stopped is True and nonempty(note), "host-confirmed stop and reason required")
        with self._edit(slug, "PAUSE") as state:
            task = self._active(state, task_id, attempt)
            require(task.get("checkpoint"), "checkpoint required before pause")
            task.update(state="WAITING", reason="INPUT_OR_RESOURCE_MISSING", note=note, attempt_id=None)
            self._summarize(state)
        return self.status(slug)

    def resume(self, slug, task_id, note):
        require(nonempty(note), "recovery evidence/note required")
        with self._edit(slug, "RESUME") as state:
            self._check_plan(slug, state)
            task = self._task(state, task_id)
            require(task["state"] == "WAITING", "task not waiting")
            if task.get("reason") == "REVIEW_BLOCKED":
                review = task["review"]
                require(review["retries"] < state["plan"]["limits"]["review_retries"], "review retries exhausted; preserve state for decision")
                review["retries"] += 1
                review["report"] = None
                task["state"] = "AWAITING_REVIEW"
            else:
                require(task.get("reason") != "GOAL_ALIGNMENT_REQUIRED", "two rounds exhausted; goal alignment required")
                require(task.get("checkpoint"), "recoverable checkpoint missing")
                for sha in task["checkpoint"]["files"].values():
                    self._read_blob(slug, sha)
                task["state"] = "READY"
            task["recovery_note"] = note
            self._summarize(state)
        return self.status(slug)

    def submit(self, slug, task_id, attempt, files, stopped=False, contributors=None):
        require(stopped is True, "host must confirm author stopped")
        require(contributors is None or isinstance(contributors, list) and all(nonempty(a) for a in contributors), "invalid contributors")
        with self._edit(slug, "SUBMIT") as state:
            task = self._task(state, task_id)
            if task.get("submission", {}).get("attempt_id") == attempt:
                require(task["submission"]["files"] == self._seal_files(slug, state, files), "duplicate submission changed payload")
                return task["submission"]
            task = self._active(state, task_id, attempt)
            require(task["round"] < 2, "two rounds exhausted")
            authors = sorted(set(task["contributors"] + (contributors or [])))
            require(all(nonempty(a) for a in authors), "invalid contributor identity")
            task["all_contributors"] = authors
            manifest = {"files": self._seal_files(slug, state, files), "attempt_id": attempt, "generation": task["generation"], "contract_digest": task["contract_digest"], "baseline_digest": task["baseline_digest"], "contributors": authors}
            sha = self._blob(slug, wire(manifest).encode())
            manifest["submission_digest"] = sha
            task.update(state="AWAITING_REVIEW", round=task["round"] + 1, submission=manifest, review=None)
            task["submissions"].append(manifest)
            self._summarize(state)
        return manifest

    def review_start(self, slug, task_id, actor):
        require(nonempty(actor), "reviewer host ID required")
        with self._edit(slug, "REVIEW_START") as state:
            self._check_plan(slug, state)
            task = self._task(state, task_id)
            require(task["state"] == "AWAITING_REVIEW", "task not awaiting review")
            require(actor not in task["submission"]["contributors"], "author/contributor cannot review own work")
            if task.get("review"):
                require(task["review"]["reviewer"] == actor, "review identity already fixed")
            else:
                task["review"] = {"review_id": uuid.uuid4().hex, "round": task["round"], "reviewer": actor, "submission_digest": task["submission"]["submission_digest"], "contract_digest": task["contract_digest"], "baseline_digest": task["baseline_digest"], "retries": 0, "report": None, "history": []}
            review = task["review"]
            result = {k: review[k] for k in ("review_id", "round", "reviewer", "submission_digest", "contract_digest", "baseline_digest")}
            result.update(acceptance=task["acceptance"], packet=self._packet(slug, state, task, "review"))
        return result

    def review(self, slug, task_id, report):
        require(isinstance(report, dict), "review report must be an object")
        with self._edit(slug, "REVIEW_REPORT") as state:
            self._check_plan(slug, state)
            task = self._task(state, task_id)
            review = task.get("review")
            require(review and task["state"] == "AWAITING_REVIEW", "no active review")
            for field in ("review_id", "round", "reviewer", "submission_digest", "contract_digest", "baseline_digest"):
                require(report.get(field) == review[field], f"review binding mismatch: {field}")
            require(report.get("stopped") is True, "host must confirm reviewer stopped")
            if review["report"]:
                require(review["report"]["payload"] == report, "review report already fixed")
                return review["report"]
            checks = report.get("checks")
            require(isinstance(checks, list) and all(isinstance(c, dict) and nonempty(c.get("acceptance_id")) for c in checks), "check objects with acceptance IDs required")
            expected = {a["id"] for a in task["acceptance"]}
            require(len(checks) == len(expected) and {c.get("acceptance_id") for c in checks} == expected, "review must cover every acceptance exactly once")
            evidence = report.get("evidence", {})
            require(isinstance(evidence, dict) and all(nonempty(k) and not k.startswith("submission:") for k in evidence), "invalid evidence IDs")
            sealed = {key: self._blob(slug, self._file(slug, state, path).read_bytes()) for key, path in evidence.items()}
            for check in checks:
                require(check.get("status") in ("PASS", "FAIL", "UNKNOWN") and nonempty(check.get("reason")), "status and reason required")
                refs = check.get("evidence_refs")
                require(isinstance(refs, list) and refs and all(nonempty(ref) for ref in refs) and len(refs) == len(set(refs)), "each check needs actual unique evidence")
                for ref in refs:
                    if ref.startswith("submission:"):
                        require(ref[11:] in task["submission"]["files"], "unknown submission evidence")
                    else:
                        require(ref in sealed, "unresolved evidence reference")
            if review["history"]:
                previous = review["history"][-1]["payload"]["checks"]
                fixed = {c["acceptance_id"]: c for c in previous if c["status"] != "UNKNOWN"}
                for check in checks:
                    if check["acceptance_id"] in fixed:
                        require(check == fixed[check["acceptance_id"]], "known findings cannot be rewritten during tool recovery")
            entry = {"payload": report, "evidence": sealed, "sha256": self._blob(slug, wire(report).encode())}
            review["report"] = entry
            review["history"].append(entry)
        return entry

    def accept(self, slug, task_id):
        with self._edit(slug, "ACCEPT") as state:
            self._check_plan(slug, state)
            task = self._task(state, task_id)
            require(task["state"] in ("AWAITING_REVIEW", "DONE"), "task not reviewable")
            submission = task["submission"]
            archived = json.loads(self._read_blob(slug, submission["submission_digest"]))
            require(archived == {k: v for k, v in submission.items() if k != "submission_digest"}, "submission manifest mismatch")
            for sha in submission["files"].values():
                self._read_blob(slug, sha)
            review = task["review"]
            require(review and review.get("report"), "independent review required")
            require(review["reviewer"] not in submission["contributors"], "self review rejected")
            entry = review["report"]
            require(json.loads(self._read_blob(slug, entry["sha256"])) == entry["payload"], "review report digest mismatch")
            for sha in entry["evidence"].values():
                self._read_blob(slug, sha)
            statuses = {c["status"] for c in entry["payload"]["checks"]}
            if task["state"] == "DONE":
                return state
            if "UNKNOWN" in statuses:
                task.update(state="WAITING", reason="REVIEW_BLOCKED")
            elif "FAIL" in statuses:
                task.update(state="READY" if task["round"] == 1 else "WAITING", reason="REWORK_REQUIRED" if task["round"] == 1 else "GOAL_ALIGNMENT_REQUIRED")
            else:
                task.update(state="DONE", reason=None, accepted={"submission_digest": submission["submission_digest"], "review_digest": entry["sha256"], "at": now()})
            self._summarize(state)
        return self.status(slug)

    def cancel(self, slug, reason, stopped=False):
        require(nonempty(reason) and stopped is True, "reason and host-confirmed stop required")
        with self._edit(slug, "CANCEL") as state:
            require(state["state"] != "DONE", "accepted project cannot be cancelled retroactively")
            for task in state["tasks"].values():
                if task["state"] != "DONE":
                    task.update(state="CANCELLED", reason=reason, attempt_id=None)
            state.update(state="CANCELLED", reason=reason)
        return self.status(slug)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parent)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    for command in ("new", "plan", "approve-plan", "dispatch", "checkpoint", "pause", "resume", "submit", "review-start", "review", "accept", "cancel", "status"):
        p = sub.add_parser(command)
        p.add_argument("project")
        if command in ("dispatch", "checkpoint", "pause", "resume", "submit", "review-start", "review", "accept"):
            p.add_argument("task")
        if command == "new":
            p.add_argument("--idea", required=True)
        if command in ("plan", "approve-plan", "review"):
            p.add_argument("--file", type=Path, required=True)
        if command in ("dispatch", "review-start"):
            p.add_argument("--actor", required=True)
        if command in ("checkpoint", "pause", "submit"):
            p.add_argument("--attempt", required=True)
        if command in ("checkpoint", "submit"):
            p.add_argument("--files", nargs="+", required=True)
        if command in ("checkpoint", "pause", "resume"):
            p.add_argument("--note", required=True)
        if command in ("pause", "submit", "cancel"):
            p.add_argument("--stopped", action="store_true")
        if command in ("dispatch", "submit"):
            p.add_argument("--contributors", nargs="*", default=[])
        if command == "cancel":
            p.add_argument("--reason", required=True)
    args = vars(parser.parse_args(argv))
    command = args.pop("command").replace("-", "_")
    bench = Workbench(args.pop("root"))
    slug = args.pop("project", None)
    task = args.pop("task", None)
    try:
        if "file" in args:
            args["plan" if command == "plan" else "report"] = json.loads(args.pop("file").read_text())
        positional = ([] if slug is None else [slug]) + ([] if task is None else [task])
        result = getattr(bench, command)(*positional, **args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (WorkflowError, OSError, KeyError, TypeError, json.JSONDecodeError, sqlite3.Error) as exc:
        print(json.dumps({"error": str(exc), "command": command}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
