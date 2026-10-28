import os
import tempfile
import time
import unittest
from reference_store import DurableStore, StateError, StaleAttempt


class DurableStoreContractTests(unittest.TestCase):
    def setUp(self):
        f = tempfile.NamedTemporaryFile(delete=False)
        self.path = f.name
        f.close()
        self.store = DurableStore(self.path)
        self.store.register_agent('agent-be', 'ENG.backend')
        self.store.register_agent('agent-fe', 'ENG.frontend')
        self.store.register_agent('agent-docs', 'ENG.docs')

    def tearDown(self):
        self.store.close()
        os.unlink(self.path)

    def make_backend(self):
        self.store.create_job('api', 'W1', 'ENG.backend', 'brief://approved-1', 'repo://api', 'a'*40,['src/'])

    def test_session_close_and_restart_rehydrates_logical_agent_progress(self):
        self.make_backend()
        first=self.store.claim('api','agent-be')
        self.store.checkpoint(first['attempt_id'], first['fence_generation'], first['session_id'],
                              'artifact://checkpoint-api-1', {'step': 'tests-red','completed': ['read-spec']})
        self.store.suspend(first['attempt_id'],first['fence_generation'],first['session_id'])
        self.store.close()
        self.store=DurableStore(self.path)  # simulate control process restart
        second=self.store.claim('api','agent-be')
        self.assertNotEqual(first['session_id'], second['session_id'])
        self.assertNotEqual(first['attempt_id'], second['attempt_id'])
        self.assertEqual(second['checkpoint_ref'],'artifact://checkpoint-api-1')
        self.assertEqual(second['checkpoint_progress']['step'],'tests-red')
        self.assertEqual(second['fence_generation'],2)
        with self.assertRaises(StaleAttempt):
            self.store.submit(first['attempt_id'],first['fence_generation'],first['session_id'],'git://old')

    def test_cross_repo_dependency_and_parallel_independent_jobs(self):
        self.make_backend()
        self.store.create_job('frontend','W1','ENG.frontend','brief://approved-1','repo://web','b'*40,['app/'],needs=['api'])
        self.store.create_job('docs','W1','ENG.docs','brief://approved-1','repo://docs','c'*40,['docs/'])
        backend=self.store.claim('api','agent-be')
        docs=self.store.claim('docs','agent-docs')
        self.assertNotEqual(backend['worktree_ref'], docs['worktree_ref'])
        with self.assertRaises(StateError):
            self.store.claim('frontend','agent-fe')
        self.store.submit(backend['attempt_id'],backend['fence_generation'],backend['session_id'],'git://api-commit')
        with self.assertRaises(StateError):
            self.store.claim('frontend','agent-fe')  # submit isn't QA success
        self.store.qa_accept('api',backend['attempt_id'],backend['fence_generation'],'evidence://api-sha-check')
        fe=self.store.claim('frontend','agent-fe')
        self.assertEqual(fe['repo_id'],'repo://web')
        self.assertEqual(fe['base_sha'],'b'*40)

    def test_expired_lease_quarantined_until_worker_stop_certified(self):
        self.make_backend()
        a=self.store.claim('api','agent-be',lease_seconds=.02)
        time.sleep(.035)
        self.assertEqual(self.store.reap_expired(),1)
        self.assertEqual(self.store.state('api')['state'],'QUARANTINED')
        with self.assertRaises(StateError):
            self.store.claim('api','agent-be')
        with self.assertRaises(StaleAttempt):
            self.store.submit(a['attempt_id'],a['fence_generation'],a['session_id'],'git://stale')
        self.store.certify_stopped('api',a['attempt_id'])
        b=self.store.claim('api','agent-be')
        self.assertEqual(b['fence_generation'],2)

    def test_wrong_agent_role_denied(self):
        self.make_backend()
        with self.assertRaises(StateError):
            self.store.claim('api','agent-fe')

    def test_duplicate_claim_denied(self):
        self.make_backend()
        self.store.claim('api','agent-be')
        with self.assertRaises(StateError):
            self.store.claim('api','agent-be')

    def test_no_empty_checkpoint_or_result(self):
        self.make_backend()
        a=self.store.claim('api','agent-be')
        with self.assertRaises(StateError):
            self.store.checkpoint(a['attempt_id'],a['fence_generation'],a['session_id'],'',{})
        with self.assertRaises(StateError):
            self.store.submit(a['attempt_id'],a['fence_generation'],a['session_id'],'')

    def test_events_survive_restart(self):
        self.make_backend()
        a=self.store.claim('api','agent-be')
        self.store.checkpoint(a['attempt_id'],a['fence_generation'],a['session_id'],'artifact://c1',{'step':'done'})
        self.store.close()
        self.store=DurableStore(self.path)
        self.assertEqual(self.store.event_types('api'), ['JOB_CREATED','ATTEMPT_CLAIMED','CHECKPOINT_SAVED'])

if __name__=='__main__':
    unittest.main()
