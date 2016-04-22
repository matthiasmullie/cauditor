from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "help_metrics.html"

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'title': 'Metrics information',
            'description': 'Detailed information about how the metrics (maintainability index, Halstead intelligent content, cyclomatic complexity, npath complexity, instability, depth of inheritance, afferent & efferent coupling) are calculated and what they mean.',
        })
        return args
