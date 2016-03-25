from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    allowed = ['question', 'project', 'author', 'score']

    def headers(self):
        if 'id' not in self.user:
            # not logged in
            self.status = "401 Unauthorized"

            return super(Controller, self).headers()

        filtered_data = dict(self.data)
        for key in self.data:
            if not key in self.allowed:
                del filtered_data[key]

        if filtered_data:
            model = models.feedback.Model(self.container.mysql)
            model.store(**filtered_data)

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        if 'id' not in self.user:
            return super(Controller, self).render(template)

        return json.dumps({})
