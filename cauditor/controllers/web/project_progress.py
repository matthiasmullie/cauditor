from cauditor.controllers.web import project_metrics
from cauditor import models


class Controller(project_metrics.Controller):
    template = "project_progress.html"
    all_commits = []

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        for commit in self.load_all_commits(self.route['project']):
            for chart in self.container.config['charts']:
                # some metrics are of type Decimal(), but I'd prefer it to be a float:
                # json is unable to serialize Decimal, and it'll cause weird output in template
                commit.update({chart['code']: float(commit[chart['code']])})
            self.all_commits.append(commit)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'all_commits': self.all_commits
        })
        return args

    def load_all_commits(self, project):
        model = models.commits.Model(self.container.mysql)
        return model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT 5000"])
