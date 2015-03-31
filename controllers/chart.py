from controllers import project


class Controller(project.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "chart.html"
        self.chart = self.load_chart(match.group(match.lastindex))
        # project & commit will be loaded in parent constructor already

    def match(self):
        """ matches /vendor/repo/chart and /vendor/repo/commit/chart """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)(/([a-f0-9]{40}))?/([a-z]+)$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'chart': self.chart,
        })
        return args

    def load_chart(self, chart):
        args = super(Controller, self).args()

        # find this specific chart's data
        data = [g for g in args['charts'] if g['code'] == chart]

        if len(data) == 0:
            raise Exception("Invalid chart")

        return data[0]
