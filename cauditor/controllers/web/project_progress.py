from cauditor.controllers.web import project_metrics


class Controller(project_metrics.Controller):
    template = "project_progress.html"
