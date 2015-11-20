from controllers import fallback


class Controller(fallback.Controller):
    template = ""

    def __init__(self):
        super(Controller, self).__init__()

        # expire session cookie
        self.cookie('session_id', self.session_data.id, -1)

    def headers(self):
        import os

        # redirect to homepage
        return [('Location', "%s://%s/" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"]))]

    def render(self, template):
        # don't render anything; we'll only be sending redirect headers
        return ""
