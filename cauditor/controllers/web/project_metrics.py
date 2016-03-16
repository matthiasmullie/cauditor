from cauditor.controllers.web import project


class Controller(project.Controller):
    template = "project_metrics.html"
    chart = None

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        self.chart = self.load_chart(self.route['chart'])

    def args(self):
        args = super(Controller, self).args()
        if not self.fail:
            args.update({
                'chart': self.chart,
                'title': self.project['name'] + ': ' + self.chart['name']
            })
        return args

    def load_chart(self, chart):
        args = super(Controller, self).args()

        # find this specific chart's data
        data = [g for g in args['charts'] if g['code'] == chart]

        if len(data) == 0:
            raise Exception("Invalid chart")

        return data[0]
