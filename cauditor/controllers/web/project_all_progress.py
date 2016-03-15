from cauditor.controllers.web import project_all_metrics


class Controller(project_all_metrics.Controller):
    template = "project_all_progress.html"
