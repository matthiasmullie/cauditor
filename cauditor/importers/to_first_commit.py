from cauditor.importers import last_commit
from cauditor import models

class Importer(last_commit.Importer):
    list_commits_command = "git log --pretty=format:'%H\t%ae\t%ad\t%ce\t%cd' --date=local {hash}"

    def __init__(self, project):
        super(Importer, self).__init__(project)

        # override commits: we want first imported commit, not last one
        try:
            commits = models.commits.Commits()
            self.commit = commits.select(project=project, options=["ORDER BY timestamp ASC", "LIMIT 1"])[0]
        except Exception:
            self.commit = None

    def execute(self):
        self.cleanup()
        self.clone(self.project['git'], self.path)
        branch = self.branch(self.path)
        commits = self.list_commits(self.path)

        previous = {}
        for i, commit in enumerate(commits):
            # we're going chronological, but DESC
            # this means the first commit will be the more recent, and
            # we need to fetch the second to compare metrics with after
            # we've done that, we'll analyze the second and get the
            # third to compare metrics with, but since we've already
            # analyzed that second commit, we can just re-use that one
            if previous:
                current = previous
            else:
                self.checkout(self.path, commit)
                current = self.analyze(self.project, self.path)

            try:
                self.checkout(self.path, commits[i+1])
                previous = self.analyze(self.project, self.path)
            except Exception:
                previous = {}

            self.listeners(self.project, branch, commit, current, previous)

        self.cleanup()
