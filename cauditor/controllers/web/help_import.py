from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = "help_import.html"

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'title': 'Import information',
            'description': 'A .cauditor.yml file lets you configure what code is analyzed. The analyzer can also be run manually, to bypass the Cauditor import queue.',
        })
        return args
