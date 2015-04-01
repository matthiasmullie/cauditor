from controllers import fallback
import models


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "project.html"
        self.project = self.load_project(match.group(1))
        self.commit = self.load_commit(match.group(1), match.group(3)) if match.group(3) is not None else {}
        self.commits = self.load_commits(match.group(1))

    def match(self):
        """ matches /vendor/repo and /vendor/repo/commit """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)(/([a-f0-9]{40}))?$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'project': self.project,
            'commit': self.commit,
            'commits': self.commits,
            'title': self.project['name']
        })
        return args

    def load_project(self, name):
        model = models.projects.Projects()
        data = model.select(name=name)
        if len(data) == 0:
            raise Exception("Invalid project")

        return data[0]

    def load_commit(self, project, hash):
        model = models.commits.Commits()
        data = model.select(project=project, hash=hash)
        if len(data) == 0:
            raise Exception("Commit not found")

        return data[0]

    def load_commits(self, project):
        model = models.commits.Commits()
        return model.select(project=project, options=["ORDER BY date DESC", "LIMIT 25"])
