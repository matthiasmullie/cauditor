from cauditor.listeners import db, aws, filesystem
from cauditor import container


def execute(project, commit, metrics):
    if db.commit_exists(commit):
        return

    config = container.load_config()
    if config['s3']['bucket'] == "":
        filesystem.execute(project, commit, metrics)
    else:
        aws.execute(project, commit, metrics)

    db.execute(project, commit, metrics)
