from cauditor.controllers.web import fallback
from cauditor.models import commits as commits_model, projects as projects_model


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
        model = projects_model.Projects()
        data = model.select(name=name)
        return next(data)

    def load_commit(self, project, hash):
        model = commits_model.Commits()
        data = model.select(project=project, hash=hash)
        return next(data)

    def load_commits(self, project):
        model = commits_model.Commits()
        commits = model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT 15"])
        return [commit for commit in commits]
