from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        # @todo: check data in post
        # @todo: check if project doesn't already exist
        # @todo: check if importable?

    def match(self):
        """ matches /api/add """
        import re
        return re.match("^/api/add$", self.uri, flags=re.IGNORECASE)

    def headers(self):
        headers = ["Content-Type: application/json"]

        # add any cookies that have to be stored
        if self.cookie_set:
            headers.insert(0, self.cookie_set)

        return headers

    def render(self):
        import json

        import os
        print(os.environ)

        # @todo: json response
        return json.dumps({'a': 'b'})
