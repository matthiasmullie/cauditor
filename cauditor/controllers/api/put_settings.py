from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    template = ""

    def __init__(self):
        super(Controller, self).__init__()
        self.project = {}

    def headers(self):
        data = self.get_input()

        model = models.settings.Settings()

        try:
            for key in data:
                model.store({
                    'user': self.user['id'],
                    'key': key,
                    'value': data[key],
                })
        except Exception:
            self.status = "401 Unauthorized"

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        model = models.settings.Settings()
        settings = model.select(user=self.user['id'])

        return json.dumps([i for i in settings])
