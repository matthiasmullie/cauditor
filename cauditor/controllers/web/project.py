from cauditor.controllers.web import fallback
from cauditor import models


class Controller(fallback.Controller):
    template = "project.html"
    project = None
    commit = None
    commits = None

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        self.project = self.load_project(self.route['project'])
        self.commit = self.load_commit(self.route['project'], self.route['commit']) if self.route['commit'] is not None else {}
        self.commits = self.load_commits(self.route['project'])

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
        model = models.projects.Model(self.container.mysql)
        data = model.select(name=name)
        return next(data)

    def load_commit(self, project, hash):
        model = models.commits.Model(self.container.mysql)
        data = model.select(project=project, hash=hash)
        return next(data)

    def load_commits(self, project):
        model = models.commits.Model(self.container.mysql)
        commits = model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT 15"])
        return [commit for commit in commits]
