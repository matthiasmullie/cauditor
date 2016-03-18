from cauditor import models
import dateutil.parser


def execute(connection, project, commit, metrics, avg, min, max):
    store_project(connection, project, commit, avg, min, max)
    store_commit(connection, commit, metrics, avg, min, max)


def commit_exists(connection, commit):
    commits = models.commits.Model(connection)
    result = commits.select(project=commit['project'], branch=commit['branch'], hash=commit['hash'])

    try:
        next(result)
        return True
    except Exception:
        return False


def get_last_commit(connection, project):
    commits = models.commits.Model(connection)
    result = commits.select(project=project['name'], branch=project['default_branch'], options=["ORDER BY timestamp DESC", "LIMIT 1"])
    return next(result)


def store_project(connection, project, commit, avg, min, max):
    try:
        last_commit = get_last_commit(connection, project)
        # comparing time strings in isoformat seems reliable enough?
        add_score = last_commit['timestamp'] < commit['timestamp'].isoformat()
    except Exception:
        add_score = True

    if add_score:
        project.update({
            # score is based on maintenance index:
            # * half the project average
            # * half the worst in the project
            'score': round((min['mi'] + avg['mi']) / 2, 2) or 0 if 'mi' in avg else 0
        })

    projects = models.projects.Model(connection)
    projects.store(project)


def store_commit(connection, commit, metrics, avg, min, max):
    commits = models.commits.Model(connection)
    commit.update({
        # metrics
        'loc': metrics['loc'] or 0 if 'loc' in metrics else 0,
        'noc': metrics['noc'] or 0 if 'noc' in metrics else 0,
        'nom': metrics['nom'] or 0 if 'nom' in metrics else 0,
        'nof': metrics['nof'] or 0 if 'nof' in metrics else 0,

        # averages
        'avg_ca': avg['ca'] or 0 if 'ca' in avg else 0,
        'avg_ce': avg['ce'] or 0 if 'ce' in avg else 0,
        'avg_i': avg['i'] or 0 if 'i' in avg else 0,
        'avg_dit': avg['dit'] or 0 if 'dit' in avg else 0,
        'avg_ccn': avg['ccn'] or 0 if 'ccn' in avg else 0,
        'avg_npath': avg['npath'] or 0 if 'npath' in avg else 0,
        'avg_he': avg['he'] or 0 if 'he' in avg else 0,
        'avg_hi': avg['hi'] or 0 if 'hi' in avg else 0,
        'avg_mi': avg['mi'] or 0 if 'mi' in avg else 0,

        # worst
        'worst_ca': max['ca'] or 0 if 'ca' in max else 0,
        'worst_ce': max['ce'] or 0 if 'ce' in max else 0,
        'worst_i': max['i'] or 0 if 'i' in max else 0,
        'worst_dit': max['dit'] or 0 if 'dit' in max else 0,
        'worst_ccn': max['ccn'] or 0 if 'ccn' in max else 0,
        'worst_npath': max['npath'] or 0 if 'npath' in max else 0,
        'worst_he': max['he'] or 0 if 'he' in max else 0,
        'worst_hi': max['hi'] or 0 if 'hi' in max else 0,
        'worst_mi': min['mi'] or 0 if 'mi' in min else 0,
    })
    commits.store(commit)
