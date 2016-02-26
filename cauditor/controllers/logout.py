from cauditor.controllers import fallback


class Controller(fallback.Controller):
    template = ""

    def __init__(self):
        super(Controller, self).__init__()

        # expire session cookie
        self.cookie('session_id', self.session_data.id, -1)

    def headers(self):
        # redirect to homepage
        return [('Location', "%s/" % self.config()['site']['host'])]

    def render(self, template="container.html"):
        # don't render anything; we'll only be sending redirect headers
        return ""
