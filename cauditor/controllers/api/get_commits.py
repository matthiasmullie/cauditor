from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    template = ""

    def render(self, template="container.html"):
        return json.dumps(self.get_commits())

    def get_commits(self):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(project=self.route['project'], branch=self.route['branch'])
        return [commit['hash'] for commit in imported]
