from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "user_feedback.html"
