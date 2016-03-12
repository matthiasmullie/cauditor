from cauditor.controllers.web import fallback
from cauditor import models


class Controller(fallback.Controller):
    template = "project.html"
    project = None
    commit = None

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        self.project = self.load_project(self.route['project'])
        if 'commit' in self.route and self.route['commit']:
            self.commit = self.load_commit(self.route['project'], self.route['commit'])
        else:
            self.commit = self.load_last_commit(self.route['project'])

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'project': self.project,
            'commit': self.commit,
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

    def load_last_commit(self, project):
        model = models.commits.Model(self.container.mysql)
        data = model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT 1"])
        return next(data)
