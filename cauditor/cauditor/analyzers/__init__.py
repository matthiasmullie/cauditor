from cauditor.analyzers import php


def execute(project, path):
    return php.analyze(project, path)
    # @todo analyzers for more programming languages...
    # @todo figure out how to process data from multiple languages, once we get there (what in db, filenames, ...)
