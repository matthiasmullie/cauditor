from controllers import fallback


class Controller(fallback.Controller):
    template = "user.html"

    def args(self):
        import models

        args = super(Controller, self).args()

        # get all of this user's active projects
        model = models.projects.Projects()
        repos = [repo['name'] for repo in args['repos']]
        projects = model.select(name=repos) if repos else []

        args.update({
            'user_projects': projects,
            'title': args['user']['name'] if args['user'] else ''
        })
        return args
