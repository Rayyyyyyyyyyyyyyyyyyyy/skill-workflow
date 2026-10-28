"""Private Git snapshots and task worktrees; never stages or resets the source repo."""
from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid


class WorkflowError(ValueError):
    pass


class GitConflict(WorkflowError):
    def __init__(self, message, info):
        super().__init__(message)
        self.info = info


def require(condition, message):
    if not condition:
        raise WorkflowError(message)


def clean(path):
    require(isinstance(path, str) and path and "\\" not in path and not Path(path).is_absolute(), "invalid Git path")
    require(all(p not in ("", ".", "..", ".git", ".workflow") for p in path.split("/")), "unsafe Git path")
    return path


def allowed(path, prefixes):
    return any(path == prefix.rstrip("/") or path.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


class GitTasks:
    def __init__(self, project, source):
        self.project = Path(project).resolve()
        self.source = Path(source).resolve()
        self.repo = self.project / ".workflow" / "git"
        self.tasks = self.project / "tasks"

    def run(self, *args, workspace=None, data=None, check=True, index=None):
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0",
                   GIT_AUTHOR_NAME="Project Workbench", GIT_AUTHOR_EMAIL="workbench@example.invalid",
                   GIT_COMMITTER_NAME="Project Workbench", GIT_COMMITTER_EMAIL="workbench@example.invalid")
        if index is not None:
            env["GIT_INDEX_FILE"] = str(index)
        command = ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "commit.gpgsign=false"]
        command += ["-C", str(workspace)] if workspace is not None else ["--git-dir=" + str(self.repo)]
        result = subprocess.run(command + list(args), input=data, capture_output=True, env=env)
        if check:
            require(result.returncode == 0, "Git failed: " + result.stderr.decode(errors="replace").strip())
        return result

    def text(self, *args, **kwargs):
        return self.run(*args, **kwargs).stdout.decode().strip()

    def check_repo(self):
        require(self.repo.is_dir() and not self.repo.is_symlink(), "private Git repository missing")
        require(self.text("rev-parse", "--is-bare-repository") == "true", "private repository must be bare")

    def check_worktree(self, info):
        self.check_repo()
        workspace = Path(info["workspace"])
        require(workspace.is_dir() and workspace.resolve().is_relative_to(self.tasks.resolve()) and not workspace.is_symlink(), "worktree outside project")
        common = Path(self.text("rev-parse", "--git-common-dir", workspace=workspace))
        if not common.is_absolute():
            common = workspace / common
        require(common.resolve() == self.repo.resolve(), "worktree belongs to another repository")
        return workspace

    def files(self, commit):
        require(isinstance(commit, str) and re.fullmatch(r"[a-f0-9]{40,64}", commit), "invalid Git commit")
        result = {}
        for entry in self.run("ls-tree", "-rz", "--full-tree", commit).stdout.split(b"\0"):
            if not entry:
                continue
            header, name = entry.split(b"\t", 1)
            mode, kind, object_id = header.decode().split()
            path = clean(name.decode())
            require(kind == "blob" and mode in ("100644", "100755"), "symlinks/submodules are not supported artifacts")
            result[path] = {"mode": mode, "object": object_id}
        return result

    def read(self, commit, path):
        clean(path)
        return self.run("show", f"{commit}:{path}").stdout

    def changed(self, base, commit):
        return sorted(p.decode() for p in self.run("diff", "--name-only", "-z", base, commit).stdout.split(b"\0") if p)

    def initialize(self, prefixes=None):
        self.repo.parent.mkdir(parents=True, exist_ok=True)
        (self.repo.parent / ".gitignore").write_text("*\n", encoding="utf-8")
        self.tasks.mkdir(parents=True, exist_ok=True)
        (self.tasks / ".gitignore").write_text("*\n", encoding="utf-8")
        if not self.repo.exists():
            result = subprocess.run(["git", "init", "--bare", str(self.repo)], capture_output=True)
            require(result.returncode == 0, "cannot create private Git repository")
        self.check_repo()
        selected = {}
        require(self.source.is_dir() and not self.source.is_symlink(), "source workspace missing")
        roots = [self.source / clean(p.rstrip("/")) for p in prefixes] if prefixes else list(self.source.iterdir())
        excluded = {".git", ".workflow", "__pycache__", ".pytest_cache"}
        for root in roots:
            require(not root.is_symlink(), "symlink source rejected")
            if not root.exists():
                continue
            paths = [root]
            if root.is_dir():
                paths = []
                for folder, dirs, names in os.walk(root, followlinks=False):
                    dirs[:] = [d for d in dirs if d not in excluded]
                    require(not any((Path(folder) / d).is_symlink() for d in dirs), "symlink source directory rejected")
                    paths.extend(Path(folder) / name for name in names)
            for path in paths:
                relative = path.relative_to(self.source).as_posix()
                if any(p in excluded for p in path.relative_to(self.source).parts):
                    continue
                clean(relative)
                require(not path.is_symlink() and path.is_file(), "source must contain regular files")
                selected[relative] = {"data": path.read_bytes(), "mode": "100755" if path.stat().st_mode & 0o111 else "100644"}
        with tempfile.TemporaryDirectory(dir=self.repo.parent) as temporary:
            index = Path(temporary) / "index"
            self.run("read-tree", "--empty", index=index)
            entries = []
            for path, item in sorted(selected.items()):
                object_id = self.text("hash-object", "-w", "--stdin", data=item["data"])
                entries.append(f"{item['mode']} {object_id}\t{path}\0".encode())
            if entries:
                self.run("update-index", "-z", "--index-info", data=b"".join(entries), index=index)
            tree = self.text("write-tree", index=index)
        commit = self.text("commit-tree", tree, "-m", "Snapshot current source bytes")
        self.run("update-ref", "refs/workbench/baselines/" + uuid.uuid4().hex, commit)
        return {"repo": str(self.repo), "baseline_commit": commit, "source": str(self.source)}

    def start(self, task_id, attempt, base, prefixes, commits=None):
        self.check_repo()
        workspace = self.tasks / f"{task_id}-{attempt}"
        branch = f"codex/{self.project.name}/{task_id}-{attempt}"
        self.run("worktree", "add", "-b", branch, str(workspace), base)
        info = {"repo": str(self.repo), "workspace": str(workspace), "branch": branch, "base_commit": base}
        if commits:
            info["merge_pending"] = list(commits)
            return self.merge(info, prefixes)
        return info

    def merge(self, info, prefixes):
        workspace = self.check_worktree(info)
        if self.run("rev-parse", "-q", "--verify", "MERGE_HEAD", workspace=workspace, check=False).returncode == 0:
            conflicts = self.run("diff", "--name-only", "--diff-filter=U", "-z", workspace=workspace).stdout
            if conflicts:
                raise GitConflict("merge conflicts must be resolved in the retained worktree", info)
            self._check_changes(info, prefixes)
            self.run("commit", "--no-gpg-sign", "-m", "Resolve accepted task integration", workspace=workspace)
            info["merge_pending"] = info["merge_pending"][1:]
        while info.get("merge_pending"):
            commit = info["merge_pending"][0]
            result = self.run("merge", "--no-ff", "--no-commit", commit, workspace=workspace, check=False)
            if result.returncode:
                raise GitConflict("accepted task integration is blocked; worktree preserved", info)
            self._check_changes(info, prefixes)
            if self.run("rev-parse", "-q", "--verify", "MERGE_HEAD", workspace=workspace, check=False).returncode == 0:
                self.run("commit", "--no-gpg-sign", "-m", "Integrate accepted task version", workspace=workspace)
            info["merge_pending"] = info["merge_pending"][1:]
        return info

    def detached(self, task_id, review_id, commit):
        workspace = self.tasks / f"{task_id}-review-{review_id}"
        self.run("worktree", "add", "--detach", str(workspace), commit)
        return {"repo": str(self.repo), "workspace": str(workspace), "base_commit": commit, "branch": None}

    def _check_changes(self, info, prefixes):
        workspace = self.check_worktree(info)
        changes = set()
        for args in (("diff", "--name-only", "-z", info["base_commit"]), ("ls-files", "--others", "--exclude-standard", "-z")):
            changes.update(p.decode() for p in self.run(*args, workspace=workspace).stdout.split(b"\0") if p)
        for path in changes:
            clean(path)
            require(allowed(path, prefixes), "task changed a path outside allowed_paths: " + path)
            cursor = workspace
            for part in Path(path).parts:
                cursor /= part
                require(not cursor.is_symlink(), "symlink task artifact rejected")
        return changes

    def commit(self, info, prefixes, files, message):
        workspace = self.check_worktree(info)
        require(self.run("merge-base", "--is-ancestor", info["base_commit"], "HEAD", workspace=workspace, check=False).returncode == 0, "task HEAD lost its fixed base")
        for path in files:
            clean(path)
            require(allowed(path, prefixes), "file outside task allowed_paths")
        self._check_changes(info, prefixes)
        self.run("add", "-A", "--", ".", workspace=workspace)
        if files:
            self.run("add", "-f", "--", *files, workspace=workspace)
        if self.run("diff", "--cached", "--quiet", workspace=workspace, check=False).returncode != 0:
            self.run("commit", "--no-gpg-sign", "-m", message, workspace=workspace)
        commit = self.text("rev-parse", "HEAD", workspace=workspace)
        changed = self.changed(info["base_commit"], commit)
        require(all(allowed(p, prefixes) for p in changed), "committed changes exceeded task scope")
        self.files(commit)
        return {**info, "commit": commit, "tree": self.text("rev-parse", commit + "^{tree}"), "changed_paths": changed}

    def verify(self, info):
        require(info.get("repo") == str(self.repo), "Git proof belongs to another project")
        require(self.text("rev-parse", info["commit"] + "^{tree}") == info["tree"], "Git tree mismatch")
        require(self.run("merge-base", "--is-ancestor", info["base_commit"], info["commit"], check=False).returncode == 0, "Git base mismatch")
        require(self.changed(info["base_commit"], info["commit"]) == info["changed_paths"], "Git change list mismatch")

    def adopt(self, workspace, base, prefixes):
        require(isinstance(base, str) and re.fullmatch(r"[a-f0-9]{40,64}", base), "adoption requires a fixed base commit ID")
        info = {"repo": str(self.repo), "workspace": str(Path(workspace).resolve()), "base_commit": base}
        path = self.check_worktree(info)
        branch = self.text("branch", "--show-current", workspace=path)
        require(branch.startswith("codex/"), "adopted task must use a codex branch")
        require(self.run("merge-base", "--is-ancestor", base, "HEAD", workspace=path, check=False).returncode == 0, "adopted worktree has another base")
        info["branch"] = branch
        self._check_changes(info, prefixes)
        return info

    def apply(self, baseline, commit):
        old, new = self.files(baseline), self.files(commit)
        paths = self.changed(baseline, commit)
        conflicts = []
        for path in paths:
            target = self.source / path
            cursor = self.source
            for part in Path(path).parts:
                cursor /= part
                require(not cursor.is_symlink(), "source symlink prevents safe apply")
            expected = self.read(baseline, path) if path in old else None
            desired = self.read(commit, path) if path in new else None
            actual = target.read_bytes() if target.is_file() else None
            mode = "100755" if target.is_file() and target.stat().st_mode & 0o111 else "100644"
            matches_old = actual == expected and (path not in old or mode == old[path]["mode"])
            matches_new = actual == desired and (path not in new or mode == new[path]["mode"])
            if not (matches_old or matches_new) or target.exists() and not target.is_file():
                conflicts.append(path)
        if conflicts:
            raise GitConflict("source changed since baseline; no files applied", {"conflicts": conflicts})
        for path in paths:
            target = self.source / path
            desired = self.read(commit, path) if path in new else None
            if (target.read_bytes() if target.is_file() else None) == desired and (path not in new or ("100755" if target.stat().st_mode & 0o111 else "100644") == new[path]["mode"]):
                continue
            if path not in new:
                target.unlink()
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
                temporary.write(self.read(commit, path))
                temporary_path = Path(temporary.name)
            temporary_path.chmod(0o755 if new[path]["mode"] == "100755" else 0o644)
            temporary_path.replace(target)
        return paths
