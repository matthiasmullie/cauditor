from cauditor.controllers.web import fallback
from cauditor import models


class Controller(fallback.Controller):
    template = "index.html"

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        if self.user:
            self.template = "index_logged_in.html"
            self.template_env.filters['score'] = self.get_score
            self.template_env.filters['rank'] = self.get_rank()

    def args(self):
        args = super(Controller, self).args()

        if self.user:
            projects = [project['name'] for project in args['imported_repos']]

            args.update({
                'commits': self.get_last_commits(projects)
            })

        return args

    def get_last_commits(self, projects):
        model = models.commits.Model(self.container.mysql)
        last_commits = {}

        for project in projects:
            commit = model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT 1"])
            try:
                last_commits.update({project: next(commit)})
            except Exception:
                # there is no commit, but that's ok, it'll be imported at some point!
                pass

        return last_commits
