from cauditor.controllers.web import fallback
import json


class Controller(fallback.Controller):
    template = ""
    data = {}

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        try:
            self.data = self.get_input()
        except Exception:
            self.data = {}

    def headers(self):
        return [('Content-Type', "application/json; charset=UTF-8")]

    def render(self, template="container.html"):
        return json.dumps({})

    def get_input(self):
        if 'wsgi.input' in self.container.environ:
            try:
                request_body_size = int(self.container.environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0

            data = self.container.environ['wsgi.input'].read(request_body_size)
            data = data.decode('utf-8')
        else:
            data = input()

        return json.loads(data)
