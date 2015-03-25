from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "user.html"

    def match(self):
        """ matches /user """
        import re
        return re.match("^/user$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'user': self.session('user'),
            'repos': self.session('repos'),
        })

        return args
