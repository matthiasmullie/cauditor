from controllers import fallback
import models


class Controller(fallback.Controller):
    template = "project.html"

    def __init__(self, project, commit=None):
        super(Controller, self).__init__()

        self.project = self.load_project(project)
        self.commit = self.load_commit(project, commit) if commit is not None else {}
        self.commits = self.load_commits(project)

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
