from cauditor.listeners import db, s3, filesystem


def execute(container, project, commit, metrics, avg, min, max):
    if db.commit_exists(container.mysql, commit):
        return

    if container.config['s3']['bucket'] == "":
        filesystem.execute(container.config, project, commit, metrics)
    else:
        s3.execute(container.config, project, commit, metrics)

    db.execute(container.mysql, project, commit, metrics, avg, min, max)
