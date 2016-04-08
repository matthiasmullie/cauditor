from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = ""

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        # expire session cookie
        self.cookie('session_id', self.session_data.id, -1)

    def headers(self):
        # redirect to homepage
        self.status = "302 Found"
        return [('Location', "%s/" % self.container.config['site']['host'])]

    def render(self, template="container.html"):
        # don't render anything; we'll only be sending redirect headers
        return ""
