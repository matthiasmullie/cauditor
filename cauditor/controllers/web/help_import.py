from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "help_import.html"
