from listeners import store_filesystem, store_db


def execute(project, branch, commit, data, previous):
    # @todo this is really poor!
    # @todo I guess the listeners should be configurable? (config.yaml)
    # @todo store_aws
    store_filesystem.execute(project, branch, commit, data, previous)
    store_db.execute(project, branch, commit, data, previous)
