from controllers import fallback
import models


class Controller(fallback.Controller):
    template = ""

    def __init__(self):
        super(Controller, self).__init__()
        self.project = {}

    def headers(self):
        import cgi

        headers = ["Content-Type: application/json; charset=UTF-8"]

        model = models.settings.Settings()

        try:
            form = cgi.FieldStorage()
            for key in form:
                model.store({
                    'user': self.user['id'],
                    'key': key,
                    'value': form[key].value,
                })
        except Exception:
            headers.append("Status: 401 Unauthorized")

        return headers

    def render(self, template):
        import json

        model = models.settings.Settings()
        settings = model.select(user=self.user['id'])

        return json.dumps([i for i in settings])
