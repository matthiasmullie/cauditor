from cauditor.controllers.web import fallback


class Controller(fallback.Controller):
    template = ""

    def args(self):
        args = super(Controller, self).args()

        args.update({
            'title': args['user']['name'] if args['user'] else ''
        })
        return args
