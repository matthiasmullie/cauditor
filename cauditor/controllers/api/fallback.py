from cauditor.controllers.web import fallback
from cauditor import container
import json


class Controller(fallback.Controller):
    template = ""

    def headers(self):
        return [('Content-Type', "application/json; charset=UTF-8")]

    def render(self, template="container.html"):
        import json
        return json.dumps({})

    def get_input(self):
        if 'wsgi.input' in container.environ:
            try:
                request_body_size = int(container.environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0

            data = container.environ['wsgi.input'].read(request_body_size)
            data = data.decode('utf-8')
        else:
            data = input()

        return json.loads(data)
