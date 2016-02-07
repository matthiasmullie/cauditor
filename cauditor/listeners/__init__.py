from cauditor.listeners import store_db, store_aws, store_filesystem
from cauditor import container


def execute(project, branch, commit, data, previous):
    # @todo this is really poor!

    config = container.load_config()
    if config['s3']['bucket'] != "None":
        store_aws.execute(project, branch, commit, data, previous)
    else:
        store_filesystem.execute(project, branch, commit, data, previous)

    store_db.execute(project, branch, commit, data, previous)
