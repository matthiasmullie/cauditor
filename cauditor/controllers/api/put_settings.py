from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    template = ""

    def headers(self):
        model = models.settings.Model(self.container.mysql)

        try:
            for key in self.data:
                model.store({
                    'user': self.user['id'],
                    'key': key,
                    'value': self.data[key],
                })
        except Exception:
            self.status = "401 Unauthorized"

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        model = models.settings.Model(self.container.mysql)
        settings = model.select(user=self.user['id'])

        return json.dumps([i for i in settings])
