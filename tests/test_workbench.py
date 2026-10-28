"""Behavior checks at the public Workbench boundary; all projects are temporary."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import workbench as workbench_module
from workbench import Workbench, WorkflowError


REPO = Path(__file__).resolve().parents[1]
RUNTIME = Path(workbench_module.__file__).resolve()


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workbench-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(REPO / "library", self.root / "library")
        for folder in ("config", "policies"):
            shutil.copytree(REPO / "runtime-reference" / folder, self.root / "runtime-reference" / folder)
        self.method_sources = self.root / "method-sources"
        self.method_sources.mkdir()
        role_path = self.root / "library" / "roles.json"
        roles = json.loads(role_path.read_text(encoding="utf-8"))
        for role_id, profile in roles["roles"].items():
            source = self.method_sources / f"{role_id}.txt"
            source.write_text(f"Fixture role {role_id}: follow the task contract.\n", encoding="utf-8")
            profile["source"] = {"path": str(source), "format": "text"}
            for index, skill in enumerate(profile.get("skills", [])):
                source = self.method_sources / f"{role_id}-skill-{index}.txt"
                source.write_text(f"Fixture skill {role_id}/{index}: keep verifiable evidence.\n", encoding="utf-8")
                skill.update(path=str(source), format="text")
        role_path.write_text(json.dumps(roles), encoding="utf-8")
        self.workbench = Workbench(self.root)
        self.slug = "small-project"
        self.workbench.new(self.slug, "Build a local text formatter; no external writes.")
        self.workspace = self.root / "projects" / self.slug / "workspace"
        self.source_workspace = self.workspace

    def plan(self, *, two_tasks=False):
        tasks = [{
            "id": "build", "playbook": "deliver", "role": "implementer",
            "allowed_paths": ["artifact.txt", "draft.txt", "linked.txt", "proof"],
            "depends_on": [], "requirement_ids": ["R1"],
            "acceptance": [{
                "id": "A1", "requirement_ids": ["R1"],
                "description": "The formatter preserves every word in the input.",
                "method": "Run the formatter against the specified example and inspect output.",
            }],
        }]
        if two_tasks:
            followup = copy.deepcopy(tasks[0])
            followup["id"] = "document"
            followup["depends_on"] = ["build"]
            followup["acceptance"][0]["id"] = "A2"
            tasks.append(followup)
        return {
            "scope": "deliver", "planner": "planner-agent",
            "routing": {"maturity": "ready", "reason": "Input, output and scope are explicit.", "missing_inputs": []},
            "requirements": [{"id": "R1", "text": "Preserve every word in the formatted output."}],
            "tasks": tasks, "limits": {"max_rounds": 2, "review_retries": 2},
        }

    def approve(self, plan=None):
        result = self.workbench.plan(self.slug, plan or self.plan())
        (self.source_workspace / "plan-review.md").write_text(
            "The plan covers R1, keeps the Playbook criteria, and limits work to local delivery.\n",
            encoding="utf-8",
        )
        self.workbench.approve_plan(self.slug, {
            "plan_hash": result["plan_hash"], "reviewer": "plan-reviewer",
            "status": "PASS", "reason": "Requirements and mandatory criteria are covered.",
            "evidence": "plan-review.md",
        })
        return result

    def dispatch(self, task_id="build", actor="author"):
        result = self.workbench.dispatch(self.slug, task_id, actor)
        self.workspace = Path(result["packet"]["workspace"])
        return result

    def submit(self, dispatch=None, task_id="build", *, text="one two three\n", contributors=None):
        dispatch = dispatch or self.dispatch(task_id)
        self.workspace = Path(dispatch["packet"]["workspace"])
        (self.workspace / "artifact.txt").write_text(text, encoding="utf-8")
        result = self.workbench.submit(
            self.slug, task_id, dispatch["attempt_id"], ["artifact.txt"],
            stopped=True, contributors=contributors,
        )
        return dispatch, result

    def review_report(self, task_id="build", actor="reviewer", status="PASS"):
        bindings = self.workbench.review_start(self.slug, task_id, actor)
        self.workspace = Path(bindings["packet"]["workspace"])
        report = {key: bindings[key] for key in (
            "review_id", "round", "submission_digest", "contract_digest", "baseline_digest", "reviewer",
        )}
        report.update({
            "checks": [{
                "acceptance_id": item["id"], "status": status,
                "reason": "Inspected the pinned artifact against this requirement.",
                "evidence_refs": ["submission:artifact.txt"],
            } for item in bindings["acceptance"]],
            "evidence": {}, "stopped": True,
        })
        return report

    def finish(self, task_id="build"):
        self.submit(task_id=task_id)
        self.workbench.review(self.slug, task_id, self.review_report(task_id))
        state = self.workbench.accept(self.slug, task_id)
        if state["plan"]["scope"] == "deliver" and all(task["state"] == "DONE" for task in state["tasks"].values()):
            state = self.workbench.apply(self.slug, task_id)
        return state

    def task(self, task_id="build"):
        return self.workbench.status(self.slug)["tasks"][task_id]

    def git(self, directory, *arguments, check=True):
        result = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "-C", str(directory), *arguments],
            capture_output=True, text=True,
        )
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def parallel_plan(self, *, conflict=False):
        plan = self.plan()
        plan["requirements"][0]["text"] = "Combine the two independently accepted local fragments without losing either change."
        prototype = plan["tasks"][0]
        tasks = []
        for task_id in ("left", "right"):
            task = copy.deepcopy(prototype)
            task.update(id=task_id, allowed_paths=["shared.txt" if conflict else f"{task_id}.txt"])
            task["acceptance"][0].update(
                id=f"A-{task_id}", description=f"The {task_id} fragment matches the specified text.",
            )
            tasks.append(task)
        integration = copy.deepcopy(prototype)
        integration.update(
            id="combine", playbook="integrate", role="integrator", depends_on=["left", "right"],
            allowed_paths=["shared.txt"] if conflict else ["left.txt", "right.txt"],
        )
        integration["acceptance"][0].update(
            id="A-combine", description="The integrated tree preserves the specified changes from both accepted commits.",
        )
        plan["tasks"] = [*tasks, integration]
        return plan

    def accept_submission(self, task_id, filenames):
        bindings = self.workbench.review_start(self.slug, task_id, f"reviewer-{task_id}")
        report = {key: bindings[key] for key in (
            "review_id", "round", "submission_digest", "contract_digest", "baseline_digest", "reviewer",
        )}
        report.update(
            stopped=True, evidence={}, checks=[{
                "acceptance_id": criterion["id"], "status": "PASS",
                "reason": "Test fixture: the specified committed fragments were independently inspected.",
                "evidence_refs": [f"submission:{name}" for name in filenames],
            } for criterion in bindings["acceptance"]],
        )
        self.workbench.review(self.slug, task_id, report)
        return self.workbench.accept(self.slug, task_id)

    def author_fragment(self, task_id, filename, content):
        dispatched = self.dispatch(task_id, f"author-{task_id}")
        (self.workspace / filename).write_text(content, encoding="utf-8")
        submission = self.workbench.submit(
            self.slug, task_id, dispatched["attempt_id"], [filename], stopped=True,
        )
        self.accept_submission(task_id, [filename])
        return dispatched, submission

    def prepare_source_git(self):
        self.git(self.root, "init", "-q")
        for filename in ("a.txt", "z.txt", "gone.txt"):
            (self.root / filename).write_text(f"committed {filename}\n", encoding="utf-8")
        self.git(self.root, "add", "--", "a.txt", "z.txt", "gone.txt")
        self.git(
            self.root, "-c", "user.name=Workbench Tests", "-c", "user.email=tests@example.invalid",
            "commit", "-q", "--no-gpg-sign", "-m", "test: initial source",
        )
        (self.root / "a.txt").write_text("user staged baseline\n", encoding="utf-8")
        self.git(self.root, "add", "--", "a.txt")
        (self.root / "z.txt").write_text("user unstaged baseline\n", encoding="utf-8")
        (self.root / "gone.txt").unlink()
        (self.root / "new.txt").write_text("user untracked input\n", encoding="utf-8")
        self.source_workspace = self.root
        self.workspace = self.root
        plan = self.plan()
        plan.update(workspace=".", allowed_paths=["a.txt", "z.txt", "gone.txt", "new.txt", "plan-review.md", "proof"])
        plan["tasks"][0]["allowed_paths"] = ["a.txt", "z.txt", "gone.txt", "new.txt", "proof"]
        self.approve(plan)
        return self.git(self.root, "rev-parse", "HEAD").stdout.strip(), (self.root / ".git/index").read_bytes()

    def test_clear_request_completes_only_after_independent_proof_acceptance(self):
        self.approve()
        self.submit()
        self.assertNotEqual(self.task()["state"], "DONE")
        report = self.review_report()
        self.assertGreater(len(report["checks"]), 1, "Playbook criteria must accompany task-specific acceptance.")
        self.workbench.review(self.slug, "build", report)
        self.assertNotEqual(self.task()["state"], "DONE", "Recording a review must not itself accept delivery.")
        self.workbench.accept(self.slug, "build")
        self.assertEqual(self.task()["state"], "DONE")

    def test_plan_must_be_independently_approved_before_dispatch(self):
        self.workbench.plan(self.slug, self.plan())
        with self.assertRaises(WorkflowError):
            self.dispatch()

    def test_missing_input_is_saved_without_starting_an_author(self):
        plan = self.plan()
        plan["routing"].update(maturity="unclear", missing_inputs=["The required output format is undecided."])
        self.workbench.plan(self.slug, plan)
        self.assertEqual(self.workbench.status(self.slug)["state"], "WAITING")
        with self.assertRaises(WorkflowError):
            self.dispatch()
        self.assertFalse(self.task().get("attempt_id"))

    def test_plan_approval_rejects_self_review_and_nonexistent_evidence(self):
        result = self.workbench.plan(self.slug, self.plan())
        (self.workspace / "plan-review.md").write_text("Checked requirement coverage.\n", encoding="utf-8")
        report = {
            "plan_hash": result["plan_hash"], "reviewer": "plan-reviewer",
            "status": "PASS", "reason": "The plan preserves all requirements.",
            "evidence": "plan-review.md",
        }
        for change in ({"reviewer": "planner-agent"}, {"evidence": "missing-plan-review.md"}):
            with self.subTest(change=change), self.assertRaises(WorkflowError):
                self.workbench.approve_plan(self.slug, {**report, **change})
        with self.assertRaises(WorkflowError):
            self.dispatch()

    def test_plan_contributor_cannot_approve_the_plan(self):
        plan = self.plan()
        plan["contributors"] = ["assistant-planner"]
        result = self.workbench.plan(self.slug, plan)
        (self.workspace / "plan-review.md").write_text("Checked requirement coverage.\n", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.workbench.approve_plan(self.slug, {
                "plan_hash": result["plan_hash"], "reviewer": "assistant-planner",
                "status": "PASS", "reason": "A contributor must not certify their own plan.",
                "evidence": "plan-review.md",
            })
        with self.assertRaises(WorkflowError):
            self.dispatch()

    def test_failed_plan_reviews_are_saved_deduplicated_and_survive_replanning_and_restart(self):
        plan = self.plan()
        for failure in (1, 2):
            plan["routing"]["reason"] = f"Candidate plan revision {failure}, with earlier findings retained."
            result = self.workbench.plan(self.slug, plan)
            evidence = f"plan-failure-{failure}.md"
            (self.workspace / evidence).write_text(
                f"Finding {failure}: an original requirement lacks sufficient verification.\n", encoding="utf-8",
            )
            report = {
                "plan_hash": result["plan_hash"], "reviewer": "plan-reviewer", "status": "FAIL",
                "reason": f"Finding {failure} blocks plan admission.", "evidence": evidence,
            }
            for _ in range(2):
                with self.assertRaises(WorkflowError):
                    self.workbench.approve_plan(self.slug, report)
                state = self.workbench.status(self.slug)
                self.assertEqual(state["plan_review_failures"], failure)
                self.assertEqual(len(state["plan_reviews"]), failure)
                self.assertEqual(state["plan_reviews"][-1]["report"], report)
            self.workbench = Workbench(self.root)
            self.assertEqual(self.workbench.status(self.slug)["plan_review_failures"], failure)
        state = self.workbench.status(self.slug)
        self.assertEqual(state["state"], "WAITING")
        self.assertEqual(state["reason"], "PLAN_ALIGNMENT_REQUIRED")
        with self.assertRaises(WorkflowError):
            self.workbench.approve_plan(self.slug, {**report, "status": "PASS", "reason": "Tool recovery cannot reset the failed-review budget."})
        plan["routing"]["reason"] = "Attempting a new plan cannot reset the failed-review budget."
        with self.assertRaises(WorkflowError):
            self.workbench.plan(self.slug, plan)
        self.assertEqual(self.workbench.status(self.slug)["plan_review_failures"], 2)

    def test_plan_rejects_uncovered_original_requirement(self):
        plan = self.plan()
        plan["requirements"].append({"id": "R2", "text": "Preserve Unicode characters."})
        with self.assertRaises(WorkflowError):
            self.workbench.plan(self.slug, plan)

    def test_plan_rejects_dependency_cycle(self):
        plan = self.plan(two_tasks=True)
        plan["tasks"][0]["depends_on"] = ["document"]
        with self.assertRaises(WorkflowError):
            self.workbench.plan(self.slug, plan)

    def test_plan_rejects_unknown_playbook_and_role(self):
        for field in ("playbook", "role"):
            with self.subTest(field=field):
                plan = self.plan()
                plan["tasks"][0][field] = "not-installed"
                with self.assertRaises(WorkflowError):
                    self.workbench.plan(self.slug, plan)

    def test_malformed_plan_shapes_are_rejected_without_changing_project_state(self):
        changes = [
            ("routing", []), ("routing", None), ("limits", []), ("limits", None),
            ("tasks", [None]), ("tasks", [42]), ("contributors", "planner"),
            ("tasks.0.role", []), ("tasks.0.depends_on", [{}]),
            ("tasks.0.requirement_ids", [{}]), ("tasks.0.acceptance", [None]),
            ("tasks.0.acceptance.0.requirement_ids", [{}]),
            ("tasks.0.supporting_sources", [None]),
            ("tasks.0.supporting_sources", [{"path": []}]),
        ]
        before = self.workbench.status(self.slug)
        for field, value in changes:
            with self.subTest(field=field, value=value):
                plan = self.plan()
                current = plan
                keys = field.split(".")
                for key in keys[:-1]:
                    current = current[int(key)] if isinstance(current, list) else current[key]
                current[int(keys[-1]) if isinstance(current, list) else keys[-1]] = value
                with self.assertRaises(WorkflowError):
                    self.workbench.plan(self.slug, plan)
                self.assertEqual(self.workbench.status(self.slug), before)

    def test_missing_role_or_skill_source_prevents_plan_admission(self):
        role_path = self.root / "library" / "roles.json"
        original = json.loads(role_path.read_text(encoding="utf-8"))
        for missing in ("role", "skill"):
            with self.subTest(missing=missing):
                roles = copy.deepcopy(original)
                profile = roles["roles"]["implementer"]
                if missing == "role":
                    profile["source"]["path"] = "method-sources/missing-role.txt"
                else:
                    profile["skills"][0]["path"] = "method-sources/missing-skill.txt"
                role_path.write_text(json.dumps(roles), encoding="utf-8")
                with self.assertRaises(WorkflowError):
                    self.workbench.plan(self.slug, self.plan())

    def test_tampered_mandatory_policy_prevents_plan_admission(self):
        policy = self.root / "runtime-reference" / "policies" / "P00-GROUNDED-ANSWER.md"
        policy.write_text("A different policy.\n", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.workbench.plan(self.slug, self.plan())

    def test_only_accepted_upstream_unlocks_followup(self):
        self.approve(self.plan(two_tasks=True))
        self.submit()
        with self.assertRaises(WorkflowError):
            self.dispatch("document")
        self.workbench.review(self.slug, "build", self.review_report())
        with self.assertRaises(WorkflowError):
            self.dispatch("document")
        self.workbench.accept(self.slug, "build")
        self.assertTrue(self.dispatch("document")["attempt_id"])

    def test_preparation_delivery_does_not_claim_the_original_project_is_finished(self):
        plan = self.plan()
        plan["scope"] = "prepare"
        plan["routing"].update(maturity="unclear", reason="A clarification brief must precede implementation.")
        plan["tasks"][0].update(playbook="clarify", role="planner")
        self.approve(plan)
        self.finish()
        state = self.workbench.status(self.slug)
        self.assertEqual(self.task()["state"], "DONE")
        self.assertEqual(state["state"], "WAITING")
        self.assertEqual(state["reason"], "DELIVERY_PLAN_REQUIRED")
        self.approve(self.plan())
        self.finish()
        self.assertEqual(self.workbench.status(self.slug)["state"], "DONE")

    def test_author_and_contributors_cannot_review_their_submission(self):
        self.approve()
        self.submit(contributors=["helper-author"])
        for actor in ("author", "helper-author"):
            with self.subTest(actor=actor), self.assertRaises(WorkflowError):
                self.workbench.review_start(self.slug, "build", actor)

    def test_previous_revision_authors_cannot_review_a_later_revision(self):
        self.approve()
        first = self.dispatch(actor="first-author")
        self.submit(first, contributors=["first-helper"])
        self.workbench.review(self.slug, "build", self.review_report(status="FAIL"))
        self.workbench.accept(self.slug, "build")
        self.submit(self.dispatch(actor="second-author"))
        for actor in ("first-author", "first-helper", "second-author"):
            with self.subTest(actor=actor), self.assertRaises(WorkflowError):
                self.workbench.review_start(self.slug, "build", actor)

    def test_dispatch_uses_pinned_role_and_skill_contents_after_source_changes(self):
        self.approve()
        role_source = self.method_sources / "implementer.txt"
        skill_source = self.method_sources / "implementer-skill-0.txt"
        expected_role = role_source.read_text(encoding="utf-8")
        expected_skill = skill_source.read_text(encoding="utf-8")
        role_source.write_text("A changed role must not silently replace the pinned role.\n", encoding="utf-8")
        skill_source.write_text("A changed skill must not silently replace the pinned skill.\n", encoding="utf-8")
        packet = self.dispatch()["packet"]
        self.assertEqual(packet["role_instructions"], expected_role)
        self.assertIn(expected_skill, packet["skill_instructions"])

    def test_dispatch_uses_pinned_supporting_source_after_original_changes(self):
        support = self.method_sources / "formatter-reference.md"
        support.write_text("Reference: preserve words and Unicode characters.\n", encoding="utf-8")
        expected = support.read_text(encoding="utf-8")
        plan = self.plan()
        plan["tasks"][0]["supporting_sources"] = [{"path": str(support), "format": "text"}]
        self.approve(plan)
        support.write_text("A later unapproved instruction.\n", encoding="utf-8")
        instructions = self.dispatch()["packet"]["supporting_instructions"]
        self.assertEqual(len(instructions), 1)
        self.assertEqual(instructions[0]["content"], expected)
        self.assertEqual(instructions[0]["source"]["path"], str(support))

    def test_missing_supporting_source_prevents_plan_admission(self):
        plan = self.plan()
        plan["tasks"][0]["supporting_sources"] = [{"path": "method-sources/not-installed.md", "format": "text"}]
        with self.assertRaises(WorkflowError):
            self.workbench.plan(self.slug, plan)
        with self.assertRaises(WorkflowError):
            self.dispatch()

    def test_review_cannot_omit_or_duplicate_a_required_acceptance(self):
        self.approve()
        self.submit()
        report = self.review_report()
        for checks in (report["checks"][:-1], report["checks"] + [report["checks"][0]]):
            with self.subTest(count=len(checks)), self.assertRaises(WorkflowError):
                self.workbench.review(self.slug, "build", {**report, "checks": checks})

    def test_malformed_reports_files_and_contributor_shapes_are_rejected(self):
        self.approve()
        for value in ([], "review", None):
            with self.subTest(plan_report=value), self.assertRaises(WorkflowError):
                self.workbench.approve_plan(self.slug, value)
        for value in ("author", [None], [{}]):
            with self.subTest(contributors=value), self.assertRaises(WorkflowError):
                self.workbench.dispatch(self.slug, "build", "author", contributors=value)
        dispatched = self.dispatch()
        for files in ([{}], [None], "artifact.txt"):
            with self.subTest(files=files), self.assertRaises(WorkflowError):
                self.workbench.submit(self.slug, "build", dispatched["attempt_id"], files, stopped=True)
        self.submit(dispatched)
        report = self.review_report()
        for value in ([], "review", None):
            with self.subTest(report=value), self.assertRaises(WorkflowError):
                self.workbench.review(self.slug, "build", value)
        invalid = [
            {**report, "checks": [None]},
            {**report, "checks": "all pass"},
            {**report, "evidence": []},
        ]
        for field, value in (("evidence_refs", [{}]), ("acceptance_id", {})):
            changed = copy.deepcopy(report)
            changed["checks"][0][field] = value
            invalid.append(changed)
        for index, changed in enumerate(invalid):
            with self.subTest(report_case=index), self.assertRaises(WorkflowError):
                self.workbench.review(self.slug, "build", changed)
        self.assertNotEqual(self.task()["state"], "DONE")

    def test_review_rejects_old_submission_or_contract_bindings(self):
        self.approve()
        self.submit()
        report = self.review_report()
        for field in ("submission_digest", "contract_digest", "baseline_digest", "review_id"):
            with self.subTest(field=field), self.assertRaises(WorkflowError):
                self.workbench.review(self.slug, "build", {**report, field: "stale-version"})

    def test_fabricated_evidence_cannot_satisfy_acceptance(self):
        self.approve()
        self.submit()
        report = self.review_report()
        report["checks"][0]["evidence_refs"] = ["missing-log"]
        report["evidence"] = {"missing-log": "not-created.txt"}
        with self.assertRaises(WorkflowError):
            self.workbench.review(self.slug, "build", report)
        self.assertNotEqual(self.task()["state"], "DONE")

    def test_workspace_mutation_does_not_replace_the_reviewed_submission(self):
        self.approve()
        _, submission = self.submit()
        (self.workspace / "artifact.txt").write_text("a later unreviewed change\n", encoding="utf-8")
        report = self.review_report()
        self.assertEqual(report["submission_digest"], submission["submission_digest"])
        self.workbench.review(self.slug, "build", report)
        self.workbench.accept(self.slug, "build")
        self.assertEqual(self.task()["state"], "DONE")

    def test_tampered_sealed_artifact_cannot_be_accepted(self):
        self.approve()
        self.submit()
        self.workbench.review(self.slug, "build", self.review_report())
        blobs = self.root / "projects" / self.slug / ".workflow" / "blobs"
        artifact = next(path for path in blobs.rglob("*") if path.is_file() and path.read_bytes() == b"one two three\n")
        artifact.chmod(0o600)
        artifact.write_text("tampered after review\n", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.workbench.accept(self.slug, "build")
        self.assertNotEqual(self.task()["state"], "DONE")

    def test_submission_rejects_missing_outside_and_symlinked_files(self):
        self.approve()
        attempt = self.dispatch()["attempt_id"]
        outside = self.root / "outside.txt"
        outside.write_text("not project data\n", encoding="utf-8")
        (self.workspace / "linked.txt").symlink_to(outside)
        for filename in ("not-created.txt", "../outside.txt", str(outside), "linked.txt"):
            with self.subTest(filename=filename), self.assertRaises(WorkflowError):
                self.workbench.submit(self.slug, "build", attempt, [filename], stopped=True)

    def test_author_must_be_host_confirmed_stopped_before_submission(self):
        self.approve()
        attempt = self.dispatch()["attempt_id"]
        (self.workspace / "artifact.txt").write_text("not yet handed off\n", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.workbench.submit(self.slug, "build", attempt, ["artifact.txt"], stopped=False)
        self.assertEqual(self.task()["state"], "RUNNING")

    def test_two_failed_rounds_preserve_history_and_block_a_third_author(self):
        self.approve()
        for expected_round in (1, 2):
            self.submit(text=f"revision {expected_round}\n")
            report = self.review_report(status="FAIL")
            self.assertEqual(report["round"], expected_round)
            self.workbench.review(self.slug, "build", report)
            self.workbench.accept(self.slug, "build")
            self.assertEqual(self.task()["state"], "READY" if expected_round == 1 else "WAITING")
        with self.assertRaises(WorkflowError):
            self.dispatch()

    def test_unknown_waits_on_same_review_and_keeps_known_failures(self):
        self.approve()
        self.submit()
        report = self.review_report()
        report["checks"][0]["status"] = "FAIL"
        report["checks"][1]["status"] = "UNKNOWN"
        self.workbench.review(self.slug, "build", report)
        self.workbench.accept(self.slug, "build")
        self.assertEqual(self.task()["state"], "WAITING")
        with self.assertRaises(WorkflowError):
            self.dispatch()
        self.workbench.resume(self.slug, "build", "The unavailable inspection source is reachable again.")
        resumed = self.workbench.review_start(self.slug, "build", "reviewer")
        self.assertEqual(resumed["review_id"], report["review_id"])
        self.assertEqual(resumed["round"], report["round"])
        altered = copy.deepcopy(report)
        altered["checks"][0]["status"] = "PASS"
        altered["checks"][1]["status"] = "PASS"
        with self.assertRaises(WorkflowError):
            self.workbench.review(self.slug, "build", altered)

    def test_review_recovery_cannot_reset_the_retry_limit_or_round(self):
        self.approve()
        self.submit()
        report = self.review_report(status="UNKNOWN")
        self.workbench.review(self.slug, "build", report)
        self.workbench.accept(self.slug, "build")
        for retry in (1, 2):
            self.workbench = Workbench(self.root)
            self.workbench.resume(self.slug, "build", f"Inspection source restored; retry {retry}.")
            bindings = self.workbench.review_start(self.slug, "build", "reviewer")
            self.assertEqual(bindings["review_id"], report["review_id"])
            self.assertEqual(bindings["round"], 1)
            self.workbench.review(self.slug, "build", report)
            self.workbench.accept(self.slug, "build")
        self.workbench = Workbench(self.root)
        with self.assertRaises(WorkflowError):
            self.workbench.resume(self.slug, "build", "Request a third retry after another restart.")
        self.assertEqual(self.task()["state"], "WAITING")

    def test_replayed_submission_and_acceptance_do_not_create_another_round(self):
        self.approve()
        dispatch, first = self.submit()
        repeated = self.workbench.submit(self.slug, "build", dispatch["attempt_id"], ["artifact.txt"], stopped=True)
        self.assertEqual(first["submission_digest"], repeated["submission_digest"])
        self.assertEqual(self.task()["round"], 1)
        self.workbench.review(self.slug, "build", self.review_report())
        self.workbench.accept(self.slug, "build")
        accepted = self.task()["accepted"]
        self.workbench.accept(self.slug, "build")
        self.assertEqual(self.task()["state"], "DONE")
        self.assertEqual(self.task()["round"], 1)
        self.assertEqual(self.task()["accepted"], accepted)

    def test_process_restart_preserves_submission_and_review_round(self):
        self.approve()
        self.submit()
        report = self.review_report()
        self.workbench = Workbench(self.root)
        self.workbench.review(self.slug, "build", report)
        self.workbench.accept(self.slug, "build")
        self.assertEqual(self.task()["state"], "DONE")

    def test_checkpoint_survives_pause_and_old_attempt_cannot_submit(self):
        self.approve()
        old_attempt = self.dispatch()["attempt_id"]
        (self.workspace / "draft.txt").write_text("recoverable partial work\n", encoding="utf-8")
        self.workbench.checkpoint(self.slug, "build", old_attempt, ["draft.txt"], "Formatting is partly complete.")
        self.workbench.pause(self.slug, "build", old_attempt, "Waiting for a detail.", stopped=True)
        self.workbench = Workbench(self.root)
        self.assertEqual(self.task()["state"], "WAITING")
        self.workbench.resume(self.slug, "build", "The missing detail has been supplied.")
        new_attempt = self.dispatch()["attempt_id"]
        self.assertNotEqual(old_attempt, new_attempt)
        with self.assertRaises(WorkflowError):
            self.workbench.submit(self.slug, "build", old_attempt, ["draft.txt"], stopped=True)

    def test_pause_resume_and_actor_changes_cannot_reset_four_attempt_limit(self):
        plan = self.plan()
        plan["limits"]["max_attempts"] = 4
        self.approve(plan)
        for generation in range(1, 5):
            attempt = self.dispatch(actor=f"author-{generation}")["attempt_id"]
            (self.workspace / "draft.txt").write_text(f"saved progress {generation}\n", encoding="utf-8")
            self.workbench.checkpoint(self.slug, "build", attempt, ["draft.txt"], "Continue from saved progress.")
            self.workbench.pause(self.slug, "build", attempt, "Waiting for input.", stopped=True)
            self.workbench = Workbench(self.root)
            self.workbench.resume(self.slug, "build", "Input supplied; retain original attempt budget.")
        self.assertEqual(self.task()["generation"], 4)
        self.assertEqual(self.task()["round"], 0)
        with self.assertRaises(WorkflowError):
            self.dispatch(actor="another-author-cannot-reset-budget")
        self.assertEqual(self.task()["generation"], 4)
        self.assertNotEqual(self.task()["state"], "DONE")

    def test_attempt_budget_must_be_positive_bounded_and_an_integer(self):
        for limit in (0, 5, True, 1.5):
            with self.subTest(limit=limit):
                plan = self.plan()
                plan["limits"]["max_attempts"] = limit
                with self.assertRaises(WorkflowError):
                    self.workbench.plan(self.slug, plan)

    def test_cancelled_project_cannot_accept_a_late_pass(self):
        self.approve()
        self.submit()
        report = self.review_report()
        self.workbench.review(self.slug, "build", report)
        self.workbench.cancel(self.slug, "User cancelled before acceptance.", stopped=True)
        with self.assertRaises(WorkflowError):
            self.workbench.accept(self.slug, "build")
        self.assertNotEqual(self.task()["state"], "DONE")

    def test_project_names_cannot_escape_collection(self):
        for slug in ("../outside", "/outside", ".", "a/b", "a\\b"):
            with self.subTest(slug=slug), self.assertRaises(WorkflowError):
                self.workbench.new(slug, "A new idea")

    def test_duplicate_project_creation_preserves_existing_idea_and_files(self):
        marker = self.workspace / "existing.txt"
        marker.write_text("keep this work\n", encoding="utf-8")
        before = self.workbench.status(self.slug)
        with self.assertRaises(WorkflowError):
            self.workbench.new(self.slug, "A different idea must not overwrite this project.")
        self.assertEqual(self.workbench.status(self.slug), before)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep this work\n")

    def test_project_state_is_persistent_sqlite_and_readable_after_restart(self):
        self.approve()
        path = self.root / "projects" / self.slug / ".workflow" / "state.sqlite3"
        self.assertTrue(path.is_file())
        with sqlite3.connect(path) as db:
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        reopened = Workbench(self.root)
        self.assertTrue(reopened.status(self.slug))
        self.assertTrue(reopened.list())

    def test_independent_tasks_run_together_in_distinct_git_worktrees(self):
        self.approve(self.parallel_plan(conflict=True))
        left = self.dispatch("left", "left-author")
        right = self.dispatch("right", "right-author")
        left_workspace = Path(left["packet"]["workspace"])
        right_workspace = Path(right["packet"]["workspace"])
        self.assertNotEqual(left_workspace, right_workspace)
        self.assertEqual(self.task("left")["state"], "RUNNING")
        self.assertEqual(self.task("right")["state"], "RUNNING")
        self.assertNotEqual(
            self.git(left_workspace, "branch", "--show-current").stdout.strip(),
            self.git(right_workspace, "branch", "--show-current").stdout.strip(),
        )
        (left_workspace / "shared.txt").write_text("left-only draft\n", encoding="utf-8")
        (right_workspace / "shared.txt").write_text("right-only draft\n", encoding="utf-8")
        self.assertEqual((left_workspace / "shared.txt").read_text(), "left-only draft\n")
        self.assertEqual((right_workspace / "shared.txt").read_text(), "right-only draft\n")
        self.assertFalse((self.source_workspace / "shared.txt").exists())

    def test_git_baseline_preserves_current_untracked_inputs_and_source_deletions(self):
        source_head, source_index = self.prepare_source_git()
        dispatched = self.dispatch()
        workspace = Path(dispatched["packet"]["workspace"])
        self.assertEqual((workspace / "a.txt").read_text(), "user staged baseline\n")
        self.assertEqual((workspace / "z.txt").read_text(), "user unstaged baseline\n")
        self.assertEqual((workspace / "new.txt").read_text(), "user untracked input\n")
        self.assertFalse((workspace / "gone.txt").exists(), "A deleted source file must not reappear from the old HEAD.")
        self.assertEqual(self.git(self.root, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual((self.root / ".git/index").read_bytes(), source_index)
        self.assertFalse((self.root / "gone.txt").exists())

    def test_accepted_parallel_commits_require_integration_proof_and_apply(self):
        self.approve(self.parallel_plan())
        _, left = self.author_fragment("left", "left.txt", "accepted left\n")
        _, right = self.author_fragment("right", "right.txt", "accepted right\n")
        self.assertNotEqual(self.workbench.status(self.slug)["state"], "DONE")
        with self.assertRaises(WorkflowError):
            self.workbench.apply(self.slug, "left")
        combined = self.dispatch("combine", "integration-author")
        workspace = Path(combined["packet"]["workspace"])
        self.assertEqual((workspace / "left.txt").read_text(), "accepted left\n")
        self.assertEqual((workspace / "right.txt").read_text(), "accepted right\n")
        submission = self.workbench.submit(
            self.slug, "combine", combined["attempt_id"], ["left.txt", "right.txt"], stopped=True,
        )
        for field in ("base_commit", "commit", "tree", "changed_paths"):
            self.assertIn(field, submission["git"])
        self.assertNotEqual(left["git"]["commit"], right["git"]["commit"])
        self.assertNotEqual(self.workbench.status(self.slug)["state"], "DONE")
        self.accept_submission("combine", ["left.txt", "right.txt"])
        self.assertNotEqual(self.workbench.status(self.slug)["state"], "DONE", "Accepted integration must still be safely applied.")
        self.workbench.apply(self.slug, "combine")
        self.assertEqual(self.workbench.status(self.slug)["state"], "DONE")
        self.assertEqual((self.source_workspace / "left.txt").read_text(), "accepted left\n")
        self.assertEqual((self.source_workspace / "right.txt").read_text(), "accepted right\n")

    def test_integration_conflict_waits_without_overwriting_source_or_author_work(self):
        (self.source_workspace / "shared.txt").write_text("source baseline\n", encoding="utf-8")
        self.approve(self.parallel_plan(conflict=True))
        left, _ = self.author_fragment("left", "shared.txt", "accepted left\n")
        right, _ = self.author_fragment("right", "shared.txt", "accepted right\n")
        try:
            self.workbench.dispatch(self.slug, "combine", "integration-author")
        except WorkflowError:
            pass  # The command may return an error after persisting the conflict.
        task = self.task("combine")
        self.assertEqual(task["state"], "WAITING")
        self.assertIn("CONFLICT", task["reason"])
        integration_workspace = Path(task["git"]["workspace"])
        self.assertTrue(integration_workspace.is_dir())
        self.assertIn("shared.txt", self.git(integration_workspace, "diff", "--name-only", "--diff-filter=U").stdout)
        self.assertEqual((self.source_workspace / "shared.txt").read_text(), "source baseline\n")
        self.assertEqual((Path(left["packet"]["workspace"]) / "shared.txt").read_text(), "accepted left\n")
        self.assertEqual((Path(right["packet"]["workspace"]) / "shared.txt").read_text(), "accepted right\n")
        with self.assertRaises(WorkflowError):
            self.workbench.apply(self.slug, "combine")
        self.assertNotEqual(self.workbench.status(self.slug)["state"], "DONE")

    def test_review_worktree_is_detached_at_the_submitted_commit(self):
        self.approve()
        dispatched, submission = self.submit()
        author_workspace = Path(dispatched["packet"]["workspace"])
        (author_workspace / "artifact.txt").write_text("a new unreviewed revision\n", encoding="utf-8")
        self.git(author_workspace, "add", "--", "artifact.txt")
        self.git(
            author_workspace, "-c", "user.name=Workbench Tests", "-c", "user.email=tests@example.invalid",
            "commit", "-q", "--no-gpg-sign", "-m", "test: later unreviewed author revision",
        )
        bindings = self.workbench.review_start(self.slug, "build", "independent-reviewer")
        review_workspace = Path(bindings["packet"]["workspace"])
        self.assertNotEqual(author_workspace, review_workspace)
        self.assertEqual(self.git(review_workspace, "rev-parse", "HEAD").stdout.strip(), submission["git"]["commit"])
        self.assertNotEqual(self.git(author_workspace, "rev-parse", "HEAD").stdout.strip(), submission["git"]["commit"])
        self.assertNotEqual(self.git(review_workspace, "symbolic-ref", "--quiet", "HEAD", check=False).returncode, 0)
        self.assertEqual((review_workspace / "artifact.txt").read_text(), "one two three\n")

    def test_apply_refuses_source_edits_without_partial_writes_or_git_metadata_changes(self):
        source_head, source_index = self.prepare_source_git()
        dispatched = self.dispatch()
        for filename in ("a.txt", "z.txt"):
            (self.workspace / filename).write_text(f"accepted replacement {filename}\n", encoding="utf-8")
        self.workbench.submit(self.slug, "build", dispatched["attempt_id"], ["a.txt", "z.txt"], stopped=True)
        self.accept_submission("build", ["a.txt", "z.txt"])
        (self.root / "z.txt").write_text("user changed this during the task\n", encoding="utf-8")
        with self.assertRaises(WorkflowError):
            self.workbench.apply(self.slug, "build")
        self.assertEqual((self.root / "a.txt").read_text(), "user staged baseline\n", "All targets must be checked before writing any target.")
        self.assertEqual((self.root / "z.txt").read_text(), "user changed this during the task\n")
        self.assertEqual(self.git(self.root, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual((self.root / ".git/index").read_bytes(), source_index)
        self.assertNotEqual(self.workbench.status(self.slug)["state"], "DONE")

    def test_safe_apply_updates_only_accepted_files_and_preserves_source_head_index_and_deletions(self):
        source_head, source_index = self.prepare_source_git()
        dispatched = self.dispatch()
        (self.workspace / "a.txt").write_text("accepted local replacement\n", encoding="utf-8")
        self.workbench.submit(self.slug, "build", dispatched["attempt_id"], ["a.txt"], stopped=True)
        self.accept_submission("build", ["a.txt"])
        self.workbench.apply(self.slug, "build")
        self.assertEqual((self.root / "a.txt").read_text(), "accepted local replacement\n")
        self.assertEqual((self.root / "z.txt").read_text(), "user unstaged baseline\n")
        self.assertEqual((self.root / "new.txt").read_text(), "user untracked input\n")
        self.assertFalse((self.root / "gone.txt").exists())
        self.assertEqual(self.git(self.root, "rev-parse", "HEAD").stdout.strip(), source_head)
        self.assertEqual((self.root / ".git/index").read_bytes(), source_index)
        self.assertEqual(self.workbench.status(self.slug)["state"], "DONE")

    def test_legacy_bootstrap_handoff_inherits_only_the_original_approved_scope(self):
        legacy_file = REPO / "tests/fixtures/workbench-pre-git.py"
        legacy_source = legacy_file.read_bytes().split(b"# --- original source follows ---\n", 1)[1]
        self.assertEqual(hashlib.sha256(legacy_source).hexdigest(), "ecec96a7f6d49960882e71dd551701cf5dbe92c6f24b4990262ed884031fda5a")
        spec = importlib.util.spec_from_file_location("legacy_workbench_fixture", legacy_file)
        legacy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(legacy_module)
        for has_project_scope in (True, False):
            with self.subTest(project_scope=has_project_scope):
                self.slug = "legacy-scoped" if has_project_scope else "legacy-unscoped"
                legacy = legacy_module.Workbench(self.root)
                legacy.new(self.slug, "Preserve the legacy build and hand off its accepted local output.")
                self.source_workspace = self.root / "projects" / self.slug / "workspace"
                (self.source_workspace / "artifact.txt").write_text("original legacy input\n", encoding="utf-8")
                plan = self.plan(two_tasks=True)
                for task in plan["tasks"]:
                    task.pop("allowed_paths")
                if has_project_scope:
                    plan["allowed_paths"] = ["artifact.txt", "draft.txt", "proof"]
                else:
                    plan["tasks"][0]["allowed_paths"] = ["artifact.txt"]
                planned = legacy.plan(self.slug, plan)
                (self.source_workspace / "plan-review.md").write_text("Fixture: checked the legacy plan before any dispatch.\n", encoding="utf-8")
                legacy.approve_plan(self.slug, {
                    "plan_hash": planned["plan_hash"], "reviewer": "legacy-plan-reviewer",
                    "status": "PASS", "reason": "Fixture legacy plan admission.", "evidence": "plan-review.md",
                })
                dispatched = legacy.dispatch(self.slug, "build", "legacy-author")
                original = legacy.status(self.slug)
                self.assertNotIn("allowed_paths", original["tasks"]["document"])
                self.assertEqual(original["tasks"]["document"]["generation"], 0)
                git = workbench_module.GitTasks(legacy.project(self.slug), self.source_workspace)
                baseline = git.initialize()
                bootstrap = git.start("build", dispatched["attempt_id"], baseline["baseline_commit"], ["artifact.txt"])
                self.workbench = Workbench(self.root)
                self.workbench.adopt_git(
                    self.slug, "build", dispatched["attempt_id"], bootstrap["workspace"], baseline["baseline_commit"],
                )
                adopted_workspace = Path(bootstrap["workspace"])
                (adopted_workspace / "artifact.txt").write_text("accepted legacy build\n", encoding="utf-8")
                submission = self.workbench.submit(
                    self.slug, "build", dispatched["attempt_id"], ["artifact.txt"], stopped=True,
                )
                self.accept_submission("build", ["artifact.txt"])
                if not has_project_scope:
                    with self.assertRaises(WorkflowError):
                        self.dispatch("document", "new-handoff-author")
                    self.assertEqual(self.task("document")["generation"], 0)
                    self.assertFalse(self.task("document").get("git"))
                    continue
                handoff = self.dispatch("document", "new-handoff-author")
                state = self.workbench.status(self.slug)
                self.assertEqual(state["plan_hash"], original["plan_hash"])
                self.assertEqual(self.task("build")["generation"], original["tasks"]["build"]["generation"])
                self.assertEqual(self.task("build")["round"], 1)
                self.assertEqual(self.task("document")["generation"], 1)
                self.assertEqual(self.task("document")["round"], 0)
                self.assertEqual(self.task("document")["allowed_paths"], plan["allowed_paths"])
                self.assertEqual(self.task("document")["git"]["base_commit"], submission["git"]["commit"])
                self.assertEqual((Path(handoff["packet"]["workspace"]) / "artifact.txt").read_text(), "accepted legacy build\n")

    def test_cli_help_new_list_and_status_work_from_another_directory(self):
        command = [sys.executable, str(RUNTIME), "--root", str(self.root)]

        def invoke(*arguments):
            result = subprocess.run(command + list(arguments), cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

        self.assertIn("approve-plan", invoke("--help"))
        created = json.loads(invoke("new", "cli-project", "--idea", "Write a local project brief."))
        self.assertEqual(created["id"], "cli-project")
        projects = json.loads(invoke("list"))
        self.assertEqual({item["id"] for item in projects}, {self.slug, "cli-project"})
        status = json.loads(invoke("status", "cli-project"))
        self.assertEqual(status["idea"], "Write a local project brief.")
        self.assertEqual(status["state"], "PLANNING")


if __name__ == "__main__":
    unittest.main()
