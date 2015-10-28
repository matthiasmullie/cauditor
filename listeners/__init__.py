from listeners import store_file, store_db


def execute(project, branch, commit, data, previous):
    # @todo this is really poor!
    # @todo I guess the listeners should be configurable? (config.yaml)
    store_file.execute(project, branch, commit, data, previous)
    store_db.execute(project, branch, commit, data, previous)
