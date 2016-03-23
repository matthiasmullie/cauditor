from cauditor.controllers.web import fallback
from cauditor import models


class Controller(fallback.Controller):
    template = "index.html"

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        if self.user:
            self.template = "index_logged_in.html"
            self.template_env.filters['score'] = self.get_score
            self.template_env.filters['rank'] = self.get_rank()

    def args(self):
        args = super(Controller, self).args()

        if self.user:
            projects = [project['name'] for project in args['imported_repos']]
            commits = self.get_commits(projects)

            args.update({
                'commits': {commit['project']: commit for commit in commits}
            })

        return args

    def get_commits(self, projects):
        model = models.commits.Model(self.container.mysql)
        return model.select(project=projects, options=["ORDER BY timestamp DESC", "LIMIT 1"])
