from cauditor.controllers import fallback
from cauditor import models


class Controller(fallback.Controller):
    template = "insight.html"

    def __init__(self):
        super(Controller, self).__init__()

        # filter out commits for which we can't find a previous commit, which could be:
        # - part of a push where not all commits were tested individually
        # - tree changes were force-pushed after parts had already been analyzed
        commits = [commit for commit in self.load_commits()] if self.settings else {}
        prev_commits = {commit['hash']: commit for commit in self.load_prev_commits(commits)}
        count = len(commits)

        self.commits = [commit for commit in commits if commit['previous'] is None or commit['previous'] in prev_commits]
        self.missing = 1 - (len(self.commits) / (count or 1))

        missing_projects = set([commit['project'] for commit in commits if commit['previous'] is not None and commit['previous'] not in prev_commits])
        self.missing_projects = [project for project in self.load_projects(missing_projects)]

        if self.missing > 10:
            # @todo fire job for missing_projects
            pass

        # calculate differences in metrics between current & previous commits
        charts = self.config()['charts']
        for commit in self.commits:
            metrics = {}
            for chart in charts:
                if commit['previous'] is None:
                    metrics.update({chart['code']: float(commit[chart['code']])})
                else:
                    metrics.update({chart['code']: float(commit[chart['code']] - prev_commits[commit['previous']][chart['code']])})

            commit.update({'diff': metrics})

    def args(self):
        args = super(Controller, self).args()

        args.update({
            'commits': self.commits,
            'missing': self.missing,
            'missing_projects': self.missing_projects,
            'title': args['user']['name'] if args['user'] else ''
        })
        return args

    def load_commits(self):
        model = models.commits.Commits()
        emails = self.settings['emails'].split(',')
        return model.select(author=emails, options=["ORDER BY timestamp DESC", "LIMIT 5000"]) if emails else {}

    def load_prev_commits(self, commits):
        if len(commits) == 0:
            return []

        model = models.commits.Commits()
        hashes = [commit['previous'] for commit in commits]
        return model.select(hash=hashes)

    def load_projects(self, projects):
        if len(projects) == 0:
            return []

        model = models.projects.Projects()
        return model.select(name=projects)
