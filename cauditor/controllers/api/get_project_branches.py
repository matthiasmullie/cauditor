from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        self.branches = self.get_branches(self.route['project'])
        if len(self.branches) == 0:
            self.status = "404 Not Found"

    def render(self, template="container.html"):
        return json.dumps(self.branches)

    def get_branches(self, project):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(project=project, columns=['branch'], options=["GROUP BY branch"])
        return [branch['branch'] for branch in imported]
