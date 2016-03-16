from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    def headers(self):
        if 'id' in self.user:
            model = models.settings.Model(self.container.mysql)
            for key in self.data:
                model.store({
                    'user': self.user['id'],
                    'key': key,
                    'value': self.data[key],
                })
        else:
            # not logged in
            self.status = "401 Unauthorized"

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        if 'id' not in self.user:
            return super(Controller, self).render(template)

        model = models.settings.Model(self.container.mysql)
        settings = model.select(user=self.user['id'])

        return json.dumps([i for i in settings])
