from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "help_metrics.html"

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'title': 'Metrics information',
            'description': 'Detailed information about how the metrics (maintainability index, cyclomatic complexity, Halstead intelligent content, instability, afferent & efferent coupling) are calculated and what they mean.',
        })
        return args
