from cauditor.controllers.web import project


class Controller(project.Controller):
    template = "project_metrics.html"

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        self.chart = self.load_chart(self.route['chart'])

    def args(self):
        args = super(Controller, self).args()
        args.update({'chart': self.chart})
        if self.commit is not None:
            args.update({
                'title': self.project['name'] + ': ' + self.chart['name'],
                'description': '%s metrics for %s' % (self.chart['name'], self.project['name'])
            })
        return args

    def load_chart(self, chart):
        args = super(Controller, self).args()

        # find this specific chart's data
        data = [g for g in args['charts'] if g['code'] == chart]

        if len(data) == 0:
            raise Exception("Invalid chart")

        return data[0]
