"""Run: python -m unittest discover -s tests -v (requires jsonschema>=4)."""
import copy
import json
import pathlib
import sys
import unittest
from datetime import datetime, timezone

from jsonschema.exceptions import ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from control.reference import (
    _canonical_digest, authorized, cleanup_allowed, hard_scope_check,
    qa_evidence_ok, result_is_current, schema_validate, skill_owner_allowed
)


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = {
            'brief': load('contracts/approved-brief.schema.json'),
            'job': load('contracts/job-attempt.schema.json'),
            'evidence': load('contracts/evidence-manifest.schema.json'),
            'message': load('a2a-compact/message.schema.json'),
        }
        cls.brief = load('examples/approved-brief.json')
        cls.job = load('examples/job.json')
        cls.attempt = load('examples/attempt.json')
        cls.manifest = load('examples/evidence-manifest.json')
        cls.task = load('examples/task.v2.json')
        cls.result = load('examples/result.v2.json')

    def test_valid_fixtures(self):
        for key, data in [('brief', self.brief), ('job', self.job),
                          ('job', self.attempt), ('evidence', self.manifest),
                          ('message', self.task), ('message', self.result)]:
            with self.subTest(key=key, kind=data.get('kind', data.get('type', ''))):
                schema_validate(data, self.schemas[key])

    def test_non_llm_issuer_required(self):
        # Mocked trusted issuer store; actual production issuer needs cryptographic or DB trust.
        now = datetime(2026, 11, 1, tzinfo=timezone.utc)
        self.assertFalse(authorized(self.brief, {}, now))
        trusted = {self.brief['authorization_ref']: {
            'brief_id': self.brief['brief_id'], 'sha256': _canonical_digest(self.brief)
        }}
        self.assertTrue(authorized(self.brief, trusted, now))
        tampered = copy.deepcopy(self.brief)
        tampered['budget_usd'] = 200
        self.assertFalse(authorized(tampered, trusted, now))
        self.assertFalse(authorized(self.brief, trusted, datetime(2027, 11, 1, tzinfo=timezone.utc)))

    def test_hard_scope_only_identifiers_paths_budget(self):
        self.assertTrue(hard_scope_check(self.job, self.brief, ['src/orders/api.py']))
        for change in [
            {'repo': 'another/repo'}, {'scope_ids': ['REQ-99']},
            {'acceptance_ids': ['AC-99']}, {'budget_usd': 30},
            {'allowed_paths': ['src/payments/']},
            {'requested_operations': ['DEPLOY_PRODUCTION']}
        ]:
            job = {**self.job, **change}
            with self.subTest(change=change):
                self.assertFalse(hard_scope_check(job, self.brief))
        for invalid in ['src/orders/../../private', 'src/orders-evil/a.py', '/src/orders/a.py', 'src\\orders\\a.py']:
            with self.subTest(path=invalid):
                self.assertFalse(hard_scope_check(self.job, self.brief, [invalid]))

    def test_scope_semantics_not_claimed_by_path_checks(self):
        # Critical caveat: changed function's user-facing behavior cannot be determined by paths.
        self.assertTrue(hard_scope_check(self.job, self.brief, ['src/orders/api.py']))
        evidence_registry = {x['evidence_ref'] for x in self.manifest['checks']}
        manifest = copy.deepcopy(self.manifest)
        manifest['checks'] = [x for x in manifest['checks'] if x['kind'] != 'SCOPE_SEMANTIC']
        self.assertFalse(qa_evidence_ok(manifest, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))

    def test_job_ready_before_first_attempt(self):
        ready = {**self.job, 'status': 'READY', 'current_attempt_id': None, 'fence_generation': 0}
        schema_validate(ready, self.schemas['job'])
        self.assertFalse(result_is_current(ready, self.attempt, self.result))

    def test_late_old_attempt_result_rejected(self):
        self.assertTrue(result_is_current(self.job, self.attempt, self.result))
        old = {**self.result, 'attempt_id': 'ATT-01-1', 'fence_generation': 1}
        schema_validate(old, self.schemas['message'])
        self.assertFalse(result_is_current(self.job, self.attempt, old))
        old_attempt = {**self.attempt, 'attempt_id': 'ATT-01-1', 'fence_generation': 1}
        self.assertFalse(result_is_current(self.job, old_attempt, old))

    def test_cancel_fence_before_cleanup(self):
        a = {**self.attempt, 'state': 'CANCEL_REQUESTED'}
        self.assertFalse(cleanup_allowed(a))
        a['write_access'] = False
        self.assertFalse(cleanup_allowed(a))
        a['process_exited'] = True
        a['state'] = 'CANCELLED'
        self.assertTrue(cleanup_allowed(a))

    def test_old_a2a_v1_rejected(self):
        no_attempt = {'v': '1', 'type': 'RESULT', 'job_id': 'JOB-01',
                      'state': 'DONE', 'artifact_refs': ['commit://abc']}
        with self.assertRaises(ValidationError):
            schema_validate(no_attempt, self.schemas['message'])

    def test_immutable_sha_gate(self):
        evidence_registry = {x['evidence_ref'] for x in self.manifest['checks']}
        self.assertTrue(qa_evidence_ok(self.manifest, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))
        self.assertFalse(qa_evidence_ok(self.manifest, self.job, self.attempt, 'b' * 40, evidence_registry, worker_id='WORKER-7'))
        tampered = copy.deepcopy(self.manifest)
        tampered['checks'][0]['subject_sha'] = 'c' * 40
        self.assertFalse(qa_evidence_ok(tampered, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))

    def test_evidence_not_a_self_attestation(self):
        evidence_registry = {x['evidence_ref'] for x in self.manifest['checks']}
        tampered = copy.deepcopy(self.manifest)
        tampered['checks'][2]['checker_id'] = 'WORKER-7'
        self.assertFalse(qa_evidence_ok(tampered, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))
        tampered = copy.deepcopy(self.manifest)
        tampered['checks'][1]['evidence_ref'] = 'artifact://fake-pass'
        self.assertFalse(qa_evidence_ok(tampered, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))
        tampered = copy.deepcopy(self.manifest)
        tampered['checks'][1]['status'] = 'FAIL'
        self.assertFalse(qa_evidence_ok(tampered, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))

    def test_cancelled_attempt_cannot_pass_qa(self):
        evidence_registry = {x['evidence_ref'] for x in self.manifest['checks']}
        attempt = {**self.attempt, 'state': 'CANCELLED', 'write_access': False}
        self.assertFalse(qa_evidence_ok(self.manifest, self.job, attempt, self.manifest['subject_sha'], evidence_registry, worker_id='WORKER-7'))

    def test_high_risk_requires_security(self):
        evidence_registry = {x['evidence_ref'] for x in self.manifest['checks']}
        self.assertFalse(qa_evidence_ok(self.manifest, self.job, self.attempt, self.manifest['subject_sha'], evidence_registry, high_risk=True, worker_id='WORKER-7'))

    def test_skill_single_owner_by_execution_mode(self):
        ownership = load('config/ownership.json')
        self.assertFalse(skill_owner_allowed('M1', 'ENG.git', 'matt:implement-spec', ownership))
        self.assertTrue(skill_owner_allowed('M1', 'ENG.foreman', 'matt:implement-spec', ownership))
        self.assertFalse(skill_owner_allowed('M1', 'QA.coordinator', 'matt:code-review', ownership))
        self.assertTrue(skill_owner_allowed('M0', 'QA.coordinator', 'matt:code-review', ownership))
        self.assertFalse(skill_owner_allowed('M0', 'QA.spec', 'matt:code-review', ownership))

if __name__ == '__main__':
    unittest.main()
