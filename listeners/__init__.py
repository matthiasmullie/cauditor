from listeners import store_file, store_db


def process(project, commit, data, previous):
    # @todo this is really poor!
    # @todo I guess the listeners should be configurable? (config.yaml)
    store_file.process(project, commit, data, previous)
    store_db.process(project, commit, data, previous)
