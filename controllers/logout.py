from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = ""

        # expire session cookie
        self.cookie('session_id', self.session_data.id, -1)

    def match(self):
        """ matches /logout """
        import re
        return re.match("^/logout$", self.uri, flags=re.IGNORECASE)

    def headers(self):
        import os

        # redirect to homepage
        return ["Location: %s://%s/" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"])]

    def render(self):
        # don't render anything; we'll only be sending redirect headers
        return ""
