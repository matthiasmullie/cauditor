from cauditor import models


def execute(connection, project, commit, metrics, avg, min, max, weighed):
    store_project(connection, project, commit, avg, min, max, weighed)
    store_commit(connection, commit, metrics, avg, min, max, weighed)


def get_last_commit(connection, project):
    commits = models.commits.Model(connection)
    result = commits.select(project=project['name'], branch=project['default_branch'], options=["ORDER BY timestamp DESC", "LIMIT 1"])
    return next(result)


def store_project(connection, project, commit, avg, min, max, weighed):
    try:
        last_commit = get_last_commit(connection, project)
        # comparing time strings in isoformat seems reliable enough?
        add_score = last_commit['timestamp'] <= commit['timestamp'].isoformat()
    except Exception:
        add_score = True

    if add_score:
        project.update({
            'score': weighed['mi']
        })

    projects = models.projects.Model(connection)
    projects.store(project)


def store_commit(connection, commit, metrics, avg, min, max, weighed):
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

        # weighed averages
        'weighed_ca': weighed['ca'] or 0 if 'ca' in weighed else 0,
        'weighed_ce': weighed['ce'] or 0 if 'ce' in weighed else 0,
        'weighed_i': weighed['i'] or 0 if 'i' in weighed else 0,
        'weighed_dit': weighed['dit'] or 0 if 'dit' in weighed else 0,
        'weighed_ccn': weighed['ccn'] or 0 if 'ccn' in weighed else 0,
        'weighed_npath': weighed['npath'] or 0 if 'npath' in weighed else 0,
        'weighed_he': weighed['he'] or 0 if 'he' in weighed else 0,
        'weighed_hi': weighed['hi'] or 0 if 'hi' in weighed else 0,
        'weighed_mi': weighed['mi'] or 0 if 'mi' in weighed else 0,
    })
    commits.store(commit)
