"""P00 deterministic enforcement reference, NOT a truth oracle or production policy engine."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def load_policy_bundle(root=ROOT):
    """Fail closed if the mandatory policy or its local file is absent."""
    root = Path(root)
    config = json.loads((root / 'config/global-policy.json').read_text(encoding='utf-8'))
    policies = config.get('required_policies') or []
    if not policies or config.get('agent_override_allowed') is not False:
        raise ValueError('POLICY_NOT_MANDATORY')
    for policy in policies:
        if policy.get('mandatory') is not True:
            raise ValueError('POLICY_NOT_MANDATORY')
        source = (root / policy['source_path']).resolve()
        if not source.is_relative_to(root.resolve()) or not source.is_file():
            raise ValueError('POLICY_SOURCE_MISSING')
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest != policy.get('policy_sha256'):
            raise ValueError('POLICY_DIGEST_MISMATCH')
        yield dict(policy, policy_sha256=digest)


def enforce_evidence_artifact(artifact, job, attempt, evidence_registry,
                              root=ROOT):
    """Validate envelope/ids/source existence; *cannot* verify semantic truth.

    evidence_registry maps immutable evidence ref -> trusted metadata record:
      {'job_id':..., 'attempt_id':..., 'subject_ref':..., 'verified': True}
    In production it MUST be populated from trusted external APIs/artifact DB, not model text.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise RuntimeError('JSONSCHEMA_DEPENDENCY_MISSING') from exc
    schema = json.loads((Path(root) / 'contracts/claim-evidence.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator(schema).validate(artifact)
    if artifact['job_id'] != job['job_id'] or artifact['attempt_id'] != attempt['attempt_id']:
        return 'BLOCK_IDENTITY_MISMATCH'
    if artifact['policy_ref'] != next(load_policy_bundle(root))['policy_ref']:
        return 'BLOCK_POLICY_MISMATCH'
    for claim in artifact['claims']:
        for ref in claim['evidence_refs']:
            record = evidence_registry.get(ref)
            if not record or record.get('verified') is not True:
                return 'BLOCK_SOURCE_UNVERIFIED'
            if record.get('subject_ref') != artifact['subject_ref']:
                return 'BLOCK_SOURCE_SCOPE'
    if artifact['verdict'] == 'SUPPORTED':
        if not artifact['claims']:
            return 'BLOCK_EMPTY_SUPPORT'
        if any(c['kind'] in ('ASSUMPTION', 'UNKNOWN') for c in artifact['claims']):
            return 'BLOCK_UNSUPPORTED_VERDICT'
        if artifact['material_contradictions']:
            return 'BLOCK_CONTRADICTION_UNRESOLVED'
    # This gate confirms evidence ref existence, not that referenced proof *logically* supports a claim.
    return 'ENVELOPE_VALID_SEMANTICS_UNVERIFIED'
