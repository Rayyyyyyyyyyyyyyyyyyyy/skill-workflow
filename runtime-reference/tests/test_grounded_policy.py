"""P00 contract tests: python -m unittest discover -s tests -v."""
import copy
import json
from pathlib import Path
import sys
import unittest

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from control.grounded_answer import load_policy_bundle, enforce_evidence_artifact


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class GroundedPolicyTests(unittest.TestCase):
    def setUp(self):
        self.config = read_json('config/global-policy.json')
        self.schema = read_json('contracts/claim-evidence.schema.json')
        self.artifact = read_json('examples/claim-evidence.json')
        self.job = {'job_id': 'JOB-17'}
        self.attempt = {'attempt_id': 'ATT-17-2'}
        self.evidence = {}

    def validate(self, artifact):
        Draft202012Validator(self.schema).validate(artifact)

    def test_policy_mandatory_and_default_denied_override(self):
        p = list(load_policy_bundle())
        self.assertEqual(p[0]['policy_ref'], 'policy://P00@1.0.0')
        self.assertTrue(p[0]['mandatory'])
        self.assertFalse(self.config['agent_override_allowed'])
        self.assertEqual(len(p[0]['policy_sha256']), 64)

    def test_bootstrap_missing_policy_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            (dest / 'config').mkdir()
            (dest / 'config/global-policy.json').write_text(json.dumps(self.config), encoding='utf-8')
            with self.assertRaises(ValueError):
                list(load_policy_bundle(dest))

    def test_tampered_policy_digest_fails_closed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            (dest / 'config').mkdir()
            (dest / 'policies').mkdir()
            (dest / 'config/global-policy.json').write_text(json.dumps(self.config), encoding='utf-8')
            (dest / 'policies/P00-GROUNDED-ANSWER.md').write_text('altered policy', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'POLICY_DIGEST_MISMATCH'):
                list(load_policy_bundle(dest))

    def test_schema_valid_unknown(self):
        self.validate(self.artifact)
        self.assertEqual(enforce_evidence_artifact(self.artifact, self.job, self.attempt, self.evidence), 'ENVELOPE_VALID_SEMANTICS_UNVERIFIED')

    def test_fact_without_evidence_rejected(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0]['kind'] = 'FACT'
        with self.assertRaises(ValidationError):
            self.validate(d)

    def test_inference_without_premise_ref_rejected(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0]['kind'] = 'INFERENCE'
        with self.assertRaises(ValidationError):
            self.validate(d)

    def test_unverified_may_not_pretend_supported(self):
        d = copy.deepcopy(self.artifact)
        d['verdict'] = 'SUPPORTED'
        self.assertEqual(enforce_evidence_artifact(d, self.job, self.attempt, self.evidence), 'BLOCK_UNSUPPORTED_VERDICT')

    def test_fabricated_evidence_ref_not_accepted(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0].update(kind='FACT', evidence_refs=['artifact://FAKE/receipt'])
        self.assertEqual(enforce_evidence_artifact(d, self.job, self.attempt, self.evidence), 'BLOCK_SOURCE_UNVERIFIED')

    def test_verified_ref_still_not_semantic_proof(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0].update(kind='FACT', evidence_refs=['artifact://JOB-17/raw.json'])
        self.evidence['artifact://JOB-17/raw.json'] = {'verified': True, 'subject_ref': d['subject_ref']}
        self.assertEqual(enforce_evidence_artifact(d, self.job, self.attempt, self.evidence), 'ENVELOPE_VALID_SEMANTICS_UNVERIFIED')

    def test_wrong_attempt_rejected(self):
        self.assertEqual(enforce_evidence_artifact(self.artifact, self.job, {'attempt_id':'ATT-17-3'}, self.evidence), 'BLOCK_IDENTITY_MISMATCH')

    def test_wrong_policy_version_rejected_by_schema(self):
        d = copy.deepcopy(self.artifact)
        d['policy_ref'] = 'policy://P00@0.0.1'
        with self.assertRaises(ValidationError):
            self.validate(d)

    def test_claim_scope_mismatch(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0].update(kind='FACT', evidence_refs=['artifact://JOB-17/other'])
        self.evidence['artifact://JOB-17/other'] = {'verified': True, 'subject_ref': 'artifact://ANOTHER'}
        self.assertEqual(enforce_evidence_artifact(d, self.job, self.attempt, self.evidence), 'BLOCK_SOURCE_SCOPE')

    def test_supported_cannot_ignore_material_contradictions(self):
        d = copy.deepcopy(self.artifact)
        d['claims'][0].update(kind='FACT', evidence_refs=['artifact://JOB-17/raw.json'])
        d['verdict'] = 'SUPPORTED'
        d['material_contradictions'] = ['Independent data conflicts']
        self.evidence['artifact://JOB-17/raw.json'] = {'verified': True, 'subject_ref': d['subject_ref']}
        self.assertEqual(enforce_evidence_artifact(d, self.job, self.attempt, self.evidence), 'BLOCK_CONTRADICTION_UNRESOLVED')


if __name__ == '__main__':
    unittest.main()
