from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    commit = {}

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        if self.route['commit'] == 'HEAD':
            self.commit = self.get_latest_commit(self.route['project'], self.route['branch'])
        else:
            self.commit = self.get_commit(self.route['project'], self.route['branch'], self.route['commit'])

        if len(self.commit) == 0:
            self.status = "404 Not Found"

    def render(self, template="container.html"):
        return json.dumps(self.commit)

    def get_latest_commit(self, project, branch):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(project=project, branch=branch, options=["ORDER BY timestamp DESC", "LIMIT 1"])
        return next(imported)

    def get_commit(self, project, branch, commit):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(project=project, branch=branch, hash=commit, options=["LIMIT 1"])
        return next(imported)
