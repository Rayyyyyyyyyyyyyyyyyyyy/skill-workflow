"""Deterministic structural checks not expressible in the JSON Schema alone."""


def validate_multi_repo_plan(plan):
    repos = [r['repo_id'] for r in plan['repos']]
    jobs = [j['job_id'] for j in plan['jobs']]
    if len(set(repos)) != len(repos) or len(set(jobs)) != len(jobs):
        raise ValueError('duplicate repository or job ID')
    by_id = {j['job_id']: j for j in plan['jobs']}
    for job in plan['jobs']:
        if job['repo_id'] not in repos:
            raise ValueError('unknown repository')
        for dep in job['depends_on']:
            if dep not in by_id:
                raise ValueError('unknown dependency')
            if dep == job['job_id']:
                raise ValueError('self dependency')
    visited, visiting = set(), set()

    def visit(job_id):
        if job_id in visiting:
            raise ValueError('dependency cycle')
        if job_id in visited:
            return
        visiting.add(job_id)
        for dep in by_id[job_id]['depends_on']:
            visit(dep)
        visiting.remove(job_id)
        visited.add(job_id)

    for job_id in jobs:
        visit(job_id)
    return True
