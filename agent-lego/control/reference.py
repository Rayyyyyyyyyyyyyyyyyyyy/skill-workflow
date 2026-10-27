"""M0 contract reference checks. For tests/examples, NOT a production policy/issuer.

Production requires transactional database CAS, a trusted auth signer/verifier,
actual runtime credential revocation, process-group shutdown and durable CI evidence.
"""
import hashlib
import json

from jsonschema import Draft202012Validator, FormatChecker


def schema_validate(payload, schema):
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(payload)


def _canonical_digest(brief):
    wire = json.dumps(brief, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(wire.encode("utf-8")).hexdigest()


def authorized(brief, trusted_receipts, now):
    """A trusted server-side receipt store must be supplied by controller, not agent."""
    from datetime import datetime
    receipt = trusted_receipts.get(brief['authorization_ref'])
    if not receipt:
        return False
    if receipt.get('brief_id') != brief['brief_id'] or receipt.get('sha256') != _canonical_digest(brief):
        return False
    start = datetime.fromisoformat(brief['issued_at'].replace('Z', '+00:00'))
    end = datetime.fromisoformat(brief['expires_at'].replace('Z', '+00:00'))
    return brief['decision_state'] == 'APPROVE' and start <= now < end


def _safe_relpath(path):
    if not isinstance(path, str) or not path or '\\' in path or path.startswith('/'):
        return False
    # Reject repeated slashes, . and .. explicitly instead of normalizing potentially ambiguous paths.
    parts = path.rstrip('/').split('/')
    return bool(parts[0]) and all(p not in ('', '.', '..') for p in parts)


def _contained(path, prefix):
    return path == prefix.rstrip('/') or path.startswith(prefix.rstrip('/') + '/')


def hard_scope_check(job, brief, changed_paths=None):
    """Checks identifiers/paths/cost only. Semantic feature scope must be reviewed separately."""
    if job['brief_id'] != brief['brief_id'] or job['repo'] != brief['repo']:
        return False
    if not set(job['scope_ids']).issubset(brief['scope_ids']):
        return False
    if not set(job['acceptance_ids']).issubset(brief['acceptance_ids']):
        return False
    if job['budget_usd'] > brief['budget_usd']:
        return False
    if not set(job['requested_operations']).issubset(brief['allowed_operations']):
        return False
    if not all(_safe_relpath(p) for p in brief['allowed_paths']):
        return False
    paths = job['allowed_paths'] + (changed_paths or [])
    return all(_safe_relpath(p) and any(_contained(p.rstrip('/'), allow.rstrip('/')) for allow in brief['allowed_paths']) for p in paths)


def result_is_current(job, attempt, result):
    """Requires atomic compare-and-set in a real controller to avoid a race."""
    return (
        job['status'] == 'RUNNING'
        and job['job_id'] == attempt['job_id'] == result['job_id']
        and job['current_attempt_id'] == attempt['attempt_id'] == result['attempt_id']
        and job['fence_generation'] == attempt['fence_generation'] == result['fence_generation']
        and attempt['state'] == 'RUNNING' and attempt['write_access'] is True
    )


def cleanup_allowed(attempt):
    """No workspace deletion while any writer may still be running."""
    return (
        attempt.get('write_access') is False
        and attempt.get('process_exited') is True
        and attempt['state'] in {'CANCELLED', 'TIMED_OUT', 'EXITED', 'FAILED', 'SUCCEEDED'}
    )


def qa_evidence_ok(manifest, job, attempt, expected_sha, evidence_registry, high_risk=False, worker_id=None):
    if job['status'] != 'RUNNING' or attempt['state'] not in {'RUNNING', 'SUCCEEDED'}:
        return False
    if manifest['job_id'] != job['job_id'] or manifest['brief_id'] != job['brief_id']:
        return False
    if manifest['attempt_id'] != attempt['attempt_id'] or manifest['fence_generation'] != attempt['fence_generation']:
        return False
    if not (job['current_attempt_id'] == attempt['attempt_id'] and job['fence_generation'] == attempt['fence_generation']):
        return False
    if manifest['repo'] != job['repo'] or manifest['subject_sha'] != expected_sha:
        return False
    required = {'TDD', 'CI', 'STANDARDS_REVIEW', 'SPEC_REVIEW', 'SCOPE_SEMANTIC'}
    if high_risk:
        required.add('SECURITY')
    status = {}
    for c in manifest['checks']:
        if c['subject_sha'] != expected_sha or c['evidence_ref'] not in evidence_registry:
            return False
        if c['kind'] in status:
            return False  # conflicting duplicated kinds must be explicitly reconciled
        status[c['kind']] = c['status']
        if c['kind'] in {'STANDARDS_REVIEW', 'SPEC_REVIEW', 'SCOPE_SEMANTIC'} and c['checker_id'] == worker_id:
            return False
    return all(status.get(k) == 'PASS' for k in required)


def skill_owner_allowed(mode, role, skill, ownership):
    expected = ownership['skill_owners_by_mode'].get(mode, {}).get(skill)
    return expected is None or expected == role
