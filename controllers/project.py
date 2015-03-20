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
        self.commit = self.load_commit(match.group(1), match.group(3))

    def match(self):
        """ matches /vendor/repo and /vendor/repo/commit """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)(/([a-f0-9]{40}))?$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'project': self.project,
            'commit': self.commit,
        })
        return args

    def load_project(self, name):
        model = models.project.Projects()
        data = model.select(name=name)
        if len(data) == 0:
            raise Exception("Invalid project")

        return data[0]

    def load_commit(self, project, hash=None):
        model = models.commit.Commits()

        if hash is None:
            data = model.select(project=project, options=['ORDER BY date DESC', "LIMIT 1"])
        else:
            data = model.select(project=project, hash=hash)

        return data[0] if len(data) > 0 else None
