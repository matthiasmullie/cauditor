from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    commits = []

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        self.commits = self.get_commits(self.route['project'], self.route['branch'])
        if len(self.commits) == 0:
            self.status = "404 Not Found"

    def render(self, template="container.html"):
        return json.dumps(self.commits)

    def get_commits(self, project, branch):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(project=project, branch=branch, options=["ORDER BY timestamp DESC"])
        return [commit for commit in imported]
