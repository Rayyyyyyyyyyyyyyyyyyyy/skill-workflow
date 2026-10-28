import copy
import json
import unittest
from pathlib import Path
from validate_plan import validate_multi_repo_plan


class MultiRepoGraphTests(unittest.TestCase):
    def setUp(self):
        self.plan=json.loads((Path(__file__).resolve().parent.parent/'examples/multi-repo-plan.json').read_text())

    def test_valid_plan(self):
        self.assertTrue(validate_multi_repo_plan(self.plan))

    def test_reject_cycle(self):
        p=copy.deepcopy(self.plan)
        p['jobs'][0]['depends_on']=['J-WEB']
        with self.assertRaisesRegex(ValueError,'cycle'):
            validate_multi_repo_plan(p)

    def test_reject_unknown_dependency(self):
        p=copy.deepcopy(self.plan)
        p['jobs'][1]['depends_on']=['J-NO']
        with self.assertRaisesRegex(ValueError,'unknown dependency'):
            validate_multi_repo_plan(p)

    def test_reject_unknown_repo(self):
        p=copy.deepcopy(self.plan)
        p['jobs'][0]['repo_id']='repo://outside'
        with self.assertRaisesRegex(ValueError,'unknown repository'):
            validate_multi_repo_plan(p)

    def test_reject_duplicate_job(self):
        p=copy.deepcopy(self.plan)
        p['jobs'].append(copy.deepcopy(p['jobs'][0]))
        with self.assertRaisesRegex(ValueError,'duplicate'):
            validate_multi_repo_plan(p)

if __name__ == '__main__':
    unittest.main()
