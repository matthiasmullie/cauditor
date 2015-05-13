from controllers import fallback


class Controller(fallback.Controller):
    template = "user.html"

    def args(self):
        args = super(Controller, self).args()

        args.update({
            'title': args['user']['name'] if args['user'] else ''
        })
        return args
