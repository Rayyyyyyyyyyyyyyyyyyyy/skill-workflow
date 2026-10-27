import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent

class DurableSchemaTests(unittest.TestCase):
    def load(self, name):
        s=json.loads((ROOT / 'contracts' / (name+'.schema.json')).read_text())
        Draft202012Validator.check_schema(s)
        return Draft202012Validator(s)

    def test_session(self):
        v=self.load('durable-session')
        example=json.loads((ROOT/'examples/durable-session.json').read_text())
        v.validate(example)
        self.assertFalse(v.is_valid({**example,'fence_generation':0}))
        self.assertFalse(v.is_valid({**example,'extra':'uncontracted'}))

    def test_checkpoint(self):
        v=self.load('durable-checkpoint')
        example=json.loads((ROOT/'examples/durable-checkpoint.json').read_text())
        v.validate(example)
        self.assertFalse(v.is_valid({**example,'api_secret':'should-never-be-here'}))
        self.assertFalse(v.is_valid({**example,'repo_sha_map':{'api':'bad-sha'}}))

    def test_multi_repo(self):
        v=self.load('multi-repo-plan')
        example=json.loads((ROOT/'examples/multi-repo-plan.json').read_text())
        v.validate(example)
        self.assertFalse(v.is_valid({**example,'repos':[]}))

if __name__ == '__main__':
    unittest.main()
