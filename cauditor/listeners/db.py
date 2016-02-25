from cauditor import models


def execute(project, commit, metrics):
    store_project(project)
    store_commit(commit, metrics)


def commit_exists(commit):
    commits = models.commits.Commits()
    result = commits.select(project=commit['project'], branch=commit['branch'], hash=commit['hash'])

    try:
        result[0]
        return True
    except Exception:
        return False


def store_project(project):
    projects = models.projects.Projects()
    projects.store(project)


def store_commit(commit, metrics):
    commits = models.commits.Commits()
    commit.update({
        # metrics
        'loc': metrics['loc'] or 0 if 'loc' in metrics else 0,
        'noc': metrics['noc'] or 0 if 'noc' in metrics else 0,
        'nom': metrics['nom'] or 0 if 'nom' in metrics else 0,
        'ca': metrics['ca'] or 0 if 'ca' in metrics else 0,
        'ce': metrics['ce'] or 0 if 'ce' in metrics else 0,
        'i': metrics['i'] or 0 if 'i' in metrics else 0,
        'dit': metrics['dit'] or 0 if 'dit' in metrics else 0,
        'ccn': metrics['ccn'] or 0 if 'ccn' in metrics else 0,
        'npath': metrics['npath'] or 0 if 'npath' in metrics else 0,
        'he': metrics['he'] or 0 if 'he' in metrics else 0,
        'hi': metrics['hi'] or 0 if 'hi' in metrics else 0,
        'mi': metrics['mi'] or 0 if 'mi' in metrics else 0,
    })
    commits.store(commit)
