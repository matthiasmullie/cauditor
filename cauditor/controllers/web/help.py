from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "help/container.html"

    def args(self):
        args = super(Controller, self).args()
        title = self.get_title()
        args.update({
            'help_template': "help/%s.html" % self.route['template'],
            'title': 'Help: %s' % title,
            'description': 'Help: %s' % title,
        })
        return args

    def get_title(self):
        prettified = self.route['template']
        prettified = prettified.replace('/', ': ')
        prettified = prettified.replace('_', ' ')
        return prettified
