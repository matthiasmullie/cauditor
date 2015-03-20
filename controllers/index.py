from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "index.html"

    def match(self):
        """ matches / """
        import re
        return re.match("^/$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            # @todo args
        })
        return args
