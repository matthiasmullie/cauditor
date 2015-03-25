from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "user.html"

    def match(self):
        """ matches /user """
        import re
        return re.match("^/user$", self.uri, flags=re.IGNORECASE)

    def args(self):
        import models

        args = super(Controller, self).args()

        # get all of this user's active projects
        model = models.projects.Projects()
        projects = model.select(name=[repo['project'] for repo in args['repos']])

        args.update({
            'user_projects': projects,
        })
        return args
