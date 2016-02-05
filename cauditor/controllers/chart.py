from cauditor.controllers import project


class Controller(project.Controller):
    template = "chart.html"

    def __init__(self, chart, project, commit=None):
        super(Controller, self).__init__(project, commit)
        # project & commit will be loaded in parent constructor

        self.chart = self.load_chart(chart)

    def args(self):
        args = super(Controller, self).args()
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
