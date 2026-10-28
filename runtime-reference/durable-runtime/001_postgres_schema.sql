-- Durable Agent Runtime draft schema (PostgreSQL 15+). NOT applied in any environment.
-- All mutations must go through an authenticated State API and transactional state machine.
-- DB rows alone do not revoke outside Git credentials or terminate OS processes.
BEGIN;
CREATE TABLE IF NOT EXISTS durable_agents (
  agent_id text PRIMARY KEY, role_id text NOT NULL,
  profile_ref text NOT NULL, policy_ref text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS durable_jobs (
  job_id text PRIMARY KEY, workflow_id text NOT NULL,
  approved_brief_ref text NOT NULL, required_role text NOT NULL,
  repo_id text NOT NULL, base_sha char(40) NOT NULL,
  allowed_paths jsonb NOT NULL,
  state text NOT NULL CHECK (state IN ('READY','RUNNING','AWAITING_QA','QUARANTINED','DONE','CANCELLED')),
  current_attempt_id uuid, fence_generation bigint NOT NULL DEFAULT 0 CHECK (fence_generation >= 0),
  checkpoint_ref text, checkpoint_progress jsonb,
  result_ref text, qa_manifest_ref text,
  version bigint NOT NULL DEFAULT 0,
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS durable_job_dependencies (
  job_id text NOT NULL REFERENCES durable_jobs(job_id),
  needs_job_id text NOT NULL REFERENCES durable_jobs(job_id),
  PRIMARY KEY (job_id, needs_job_id),
  CHECK (job_id <> needs_job_id)
);
CREATE TABLE IF NOT EXISTS durable_attempts (
  attempt_id uuid PRIMARY KEY, job_id text NOT NULL REFERENCES durable_jobs(job_id),
  agent_id text NOT NULL REFERENCES durable_agents(agent_id),
  fence_generation bigint NOT NULL CHECK (fence_generation > 0),
  state text NOT NULL CHECK (state IN ('RUNNING','SUBMITTED','SUPERSEDED','EXPIRED','FAILED')),
  lease_until timestamptz NOT NULL, worktree_ref text NOT NULL,
  session_id uuid NOT NULL UNIQUE,
  UNIQUE (job_id, fence_generation)
);
CREATE TABLE IF NOT EXISTS durable_sessions (
  session_id uuid PRIMARY KEY, attempt_id uuid NOT NULL UNIQUE REFERENCES durable_attempts(attempt_id),
  agent_id text NOT NULL REFERENCES durable_agents(agent_id),
  created_at timestamptz NOT NULL DEFAULT now(), closed_at timestamptz
);
CREATE TABLE IF NOT EXISTS durable_events (
  event_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  event_key text NOT NULL UNIQUE,
  job_id text NOT NULL REFERENCES durable_jobs(job_id),
  attempt_id uuid,
  event_type text NOT NULL, payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);
-- Outbox for idempotent external delivery. External receiver needs idempotency enforcement too.
CREATE TABLE IF NOT EXISTS durable_outbox (
  outbox_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  idempotency_key text NOT NULL UNIQUE,
  event_type text NOT NULL, payload jsonb NOT NULL,
  state text NOT NULL DEFAULT 'PENDING' CHECK (state IN ('PENDING','SENT','FAILED')),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_durable_jobs_state ON durable_jobs(state, updated_at);
CREATE INDEX IF NOT EXISTS idx_durable_attempts_lease ON durable_attempts(lease_until) WHERE state='RUNNING';
CREATE INDEX IF NOT EXISTS idx_durable_deps_needs ON durable_job_dependencies(needs_job_id);
COMMIT;
-- Provision rules: CREATE new attempt + update durable_jobs.current_attempt_id and fence
-- + append durable_events/outbox in a single transaction. Claim with FOR UPDATE SKIP LOCKED
-- and verify dependencies, ApprovedBrief, role and resource policy before committing.
