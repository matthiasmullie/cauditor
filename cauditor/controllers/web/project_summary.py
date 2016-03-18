from cauditor.controllers.web import project
from cauditor import models


class Controller(project.Controller):
    template = "project_summary.html"
    commits = {}
    prev_commits = {}
    batch_size = 30

    def __init__(self, route, cookies, session, container):
        super(Controller, self).__init__(route, cookies, session, container)

        self.commits = self.load_commits(self.route['project'], self.batch_size)
        self.prev_commits = {commit['hash']: commit for commit in self.load_prev_commits(self.commits)}

        self.template_env.filters['score'] = self.get_score
        self.template_env.filters['rank'] = self.get_rank()

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'commits': self.commits,
            'prev_commits': self.prev_commits,
            'batch_size': self.batch_size,
        })
        return args

    def load_commits(self, project, limit):
        model = models.commits.Model(self.container.mysql)
        commits = model.select(project=project, options=["ORDER BY timestamp DESC", "LIMIT "+str(limit)])
        return [commit for commit in commits]

    def load_prev_commits(self, commits):
        if len(commits) == 0:
            return []

        model = models.commits.Model(self.container.mysql)
        hashes = [commit['previous'] for commit in commits]
        return model.select(project=commits[0]['project'], hash=hashes)

    def get_score(self, commit):
        return round((2 * commit['worst_mi'] + commit['avg_mi']) / 3, 2)

    def get_rank(self):
        scores = []
        model = models.projects.Model(self.container.mysql)
        projects = model.select(options=['ORDER BY score DESC'])
        for project in projects:
            scores.append(project['score'])

        def rank_calculator(score):
            better = 0
            for i in scores:
                if i > score:
                    better += 1
                else:
                    break

            # calculate the amount of projects that score worst than this score
            return 100 * (1 - better / len(scores) or 1)\

        return rank_calculator
