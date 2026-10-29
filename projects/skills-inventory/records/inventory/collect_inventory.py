"""Read Skill metadata; never install or execute a Skill. Requires existing rg/PyYAML."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

import yaml


def classify(path: Path, home: Path) -> str:
    value = path.relative_to(home).as_posix()
    if value.startswith('.codex/skills/.system/'):
        return 'codex-system'
    if value.startswith('.codex/skills/'):
        return 'codex-personal'
    if value.startswith('.claude/skills/synced/'):
        return 'claude-synced'
    if value.startswith('.claude/skills/'):
        return 'claude-personal'
    if value.startswith('.agents/skills/'):
        return 'shared-personal'
    if value.startswith(('.codex/skill-backups/', '.agents/skill-backups/')):
        return 'backup'
    if value.startswith('.codex/.tmp/'):
        return 'temporary-cache'
    if value.startswith('.codex/plugins/cache/'):
        return 'codex-plugin-cache'
    if value.startswith('.claude/plugins/cache/'):
        return 'claude-plugin-cache'
    if value.startswith(('.claude/plugins/marketplaces/', '.codex/plugins/marketplaces/')):
        return 'marketplace-source'
    if value.startswith('.codex/vendor_imports/'):
        return 'vendor-source'
    if value.startswith('.cache/codex-runtimes/'):
        return 'runtime-bundled'
    if '/projects/' in value and '/tasks/' in value:
        return 'task-worktree'
    if value.startswith('workflow/.claude/skills/'):
        return 'current-repo'
    if value.startswith('workflow/runtime-reference/'):
        return 'reference-component'
    return 'other-project-source'


def scan(roots: list[Path], follow: bool) -> subprocess.CompletedProcess:
    command = ['rg', '--files', '--hidden', '--no-ignore']
    if follow:
        command.append('--follow')
    for glob in ('SKILL.md', '!**/Library/**', '!**/.Trash/**', '!**/node_modules/**',
                 '!**/.git/**', '!**/.workflow/**', '!**/__pycache__/**'):
        command.extend(['-g', glob])
    command.extend(str(p) for p in roots)
    return subprocess.run(command, capture_output=True, text=True)


def summarize(rows):
    grouped = Counter(r['source_group'] for r in rows)
    by_name = defaultdict(list)
    for row in rows:
        by_name[row['name']].append(row)
    return {
        'definition_paths': len(rows),
        'canonical_files': len({r['canonical_path'] for r in rows}),
        'distinct_declared_names': len(by_name),
        'distinct_contents': len({r['sha256'] for r in rows}),
        'symlink_alias_paths': sum(r['is_symlink_alias'] for r in rows),
        'source_group_counts': dict(sorted(grouped.items())),
        'names_with_multiple_paths': sum(len(v) > 1 for v in by_name.values()),
        'names_with_different_contents': sum(len({r['sha256'] for r in v}) > 1 for v in by_name.values()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    home = args.home.resolve()
    out = args.output.resolve()
    protected = ('skills.json', 'skills.csv', 'scan-home-paths.txt', 'scan-home-errors.txt', 'scan-follow-paths.txt', 'scan-follow-errors.txt')
    if any((out / name).exists() for name in protected):
        parser.error('output already contains an inventory snapshot; choose a new --output directory')
    out.mkdir(parents=True, exist_ok=True)
    started = datetime.now(ZoneInfo('Asia/Taipei')).isoformat()
    home_scan = scan([home], False)
    follow_roots = [home / p for p in (
        '.codex/skills', '.claude/skills', '.agents/skills', '.codex/plugins',
        '.claude/plugins', '.codex/vendor_imports', '.codex/.tmp') if (home / p).is_dir()]
    follow_scan = scan(follow_roots, True)
    for label, result in [('home', home_scan), ('follow', follow_scan)]:
        (out / f'scan-{label}-paths.txt').write_text(result.stdout)
        (out / f'scan-{label}-errors.txt').write_text(result.stderr)
        if result.returncode not in (0, 1, 2):
            raise RuntimeError(f'{label} scan failed: exit {result.returncode}')
    paths = sorted(set(home_scan.stdout.splitlines()) | set(follow_scan.stdout.splitlines()))
    rows = []
    errors = []
    for raw in paths:
        path = Path(raw)
        try:
            data = path.read_bytes()
            text = data.decode('utf-8-sig')
            normalized = text.replace('\r\n', '\n')
            if not normalized.startswith('---\n'):
                raise ValueError('no YAML frontmatter')
            front = normalized.split('\n---', 1)[0][4:]
            metadata = yaml.safe_load(front)
            if not isinstance(metadata, dict):
                raise ValueError('frontmatter is not an object')
            if not isinstance(metadata.get('name'), str):
                raise ValueError('missing string name')
            canonical = path.resolve(strict=True)
            alias_components = [str(p) for p in [path, *path.parents] if p.is_symlink()]
            description = metadata.get('description', '')
            if not isinstance(description, str):
                description = json.dumps(description, ensure_ascii=False, default=str)
            rows.append({
                'name': metadata['name'],
                'description': description,
                'path': str(path),
                'canonical_path': str(canonical),
                'source_group': classify(path, home),
                'sha256': hashlib.sha256(data).hexdigest(),
                'bytes': len(data),
                'modified_utc': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
                'is_symlink_alias': bool(alias_components),
                'symlink_components': alias_components,
                'disable_model_invocation': metadata.get('disable-model-invocation'),
                'user_invocable': metadata.get('user-invocable'),
                'declared_license': metadata.get('license'),
                'loaded_or_enabled': 'UNKNOWN: presence only; runtime/config not audited',
            })
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
            errors.append({'path': str(path), 'error': str(exc)})
    summary = summarize(rows)
    report = {
        'snapshot_started_taipei': started,
        'snapshot_finished_taipei': datetime.now(ZoneInfo('Asia/Taipei')).isoformat(),
        'scope': {'home': str(home), 'follow_symlinks_in_roots': [str(p) for p in follow_roots],
                  'excluded_directory_names': ['Library', '.Trash', 'node_modules', '.git', '.workflow', '__pycache__'],
                  'not_scanned': ['system-wide directories outside the user home', 'excluded directories', 'arbitrary symlink directories outside the explicitly followed roots'],
                  'metadata_only': True, 'skill_bodies_executed': False,
                  'runtime_enabled_config_audited': False},
        'scan_results': {'home': {'exit_code': home_scan.returncode, 'paths': len(home_scan.stdout.splitlines()), 'errors': home_scan.stderr.splitlines()},
                         'follow': {'exit_code': follow_scan.returncode, 'paths': len(follow_scan.stdout.splitlines()), 'errors': follow_scan.stderr.splitlines()}},
        'collector_dependencies': {'python': sys.version.split()[0], 'pyyaml': importlib.metadata.version('PyYAML'), 'rg': subprocess.check_output(['rg', '--version'], text=True).splitlines()[0]},
        'count_definitions': {
            'definition_paths': 'Unique lexical SKILL.md paths discovered by the recorded scans, including explicit symlink aliases.',
            'canonical_files': 'Unique strict Path.resolve() strings; not plugin-installation, semantic or inode-level deduplication.',
            'distinct_declared_names': 'Exact YAML name strings, case-sensitive; no semantic synonym merging.',
            'distinct_contents': 'Unique SHA-256 of complete SKILL.md bytes, not independently validated capabilities.',
        },
        'summary': summary, 'metadata_errors': errors, 'skills': rows,
    }
    (out / 'skills.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + '\n')
    columns = ['name', 'description', 'source_group', 'path', 'canonical_path', 'sha256', 'bytes', 'modified_utc', 'is_symlink_alias', 'disable_model_invocation', 'user_invocable', 'declared_license', 'loaded_or_enabled']
    with (out / 'skills.csv').open('w', newline='', encoding='utf-8-sig') as target:
        writer = csv.DictWriter(target, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    assert len(paths) == len(rows) + len(errors)
    assert len(rows) == len({r['path'] for r in rows})
    assert sum(summary['source_group_counts'].values()) == len(rows)
    assert all(r['canonical_path'] and len(r['sha256']) == 64 for r in rows)
    assert classify(home / '.claude/skills/synced/x/SKILL.md', home) == 'claude-synced'
    assert classify(home / '.codex/skills/.system/x/SKILL.md', home) == 'codex-system'
    assert classify(home / 'workflow/projects/x/tasks/y/.claude/skills/z/SKILL.md', home) == 'task-worktree'
    print(json.dumps({'summary': summary, 'metadata_errors': len(errors), 'scan_exit_codes': [home_scan.returncode, follow_scan.returncode]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
