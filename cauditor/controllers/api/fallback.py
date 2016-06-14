from cauditor.controllers.web import fallback
import json


class Controller(fallback.Controller):
    template = ""

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        try:
            self.data = self.get_input()
        except Exception:
            self.data = {}

        # all controllers extend from this one, so I'm going to special-case
        # the 404 header
        self.status = "404 Not Found" if self.__module__ == "cauditor.controllers.api.fallback" else "200 OK"

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
