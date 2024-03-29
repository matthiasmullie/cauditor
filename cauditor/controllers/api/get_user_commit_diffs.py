from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        # init here, because we'll only want to validate (and use) the incoming data after
        # we're sure this is the controller we're router to (which may not be this one
        # after all, eventually!)
        self.diffs = []

    def headers(self):
        if 'id' not in self.user:
            # not logged in
            self.status = "401 Unauthorized"

            return super(Controller, self).headers()

        emails = self.settings['emails'].split(',')
        commits = self.get_commits(emails)
        prev_commits = self.get_prev_commits(commits)

        commits = [commit for commit in commits if commit['previous'] is None or commit['previous'] in prev_commits]

        for commit in commits:
            # filter out commits we couldn't find previous commit for
            if commit['previous'] is None or commit['previous'] not in prev_commits:
                continue

            diff = self.get_commit_diff(commit, prev_commits[commit['previous']])
            self.diffs.append(diff)

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        return json.dumps(self.diffs)

    def get_commits(self, emails):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(author=emails, options=["ORDER BY timestamp DESC"])
        return [commit for commit in imported]

    def get_prev_commits(self, commits):
        if len(commits) == 0:
            return []

        model = models.commits.Model(self.container.mysql)
        hashes = [commit['previous'] for commit in commits]
        prev_commits = model.select(hash=hashes)
        return {commit['hash']: commit for commit in prev_commits}

    def get_commit_diff(self, commit, prev_commit):
        data = {
            'hash': commit['hash'],
            'timestamp': commit['timestamp'],
            'project': commit['project'],
            'branch': commit['branch'],
        }

        for chart in self.container.config['charts']:
            # we store averages, but we want to know the absolute impact of a commit,
            # not relative to the rest of the codebase
            # if we multiply the average metric score with the amount of methods or
            # classes, we'll get the project-wide total metric value, which we can
            # then compare to the previous commit to see the actual change
            multiplier = commit['nom'] + commit['nof'] if chart['basis'] == 'method' else commit['noc']
            prev_multiplier = prev_commit['nom'] + prev_commit['nof'] if chart['basis'] == 'method' else prev_commit['noc']

            cur = commit['avg_'+chart['code']] * multiplier
            prev = prev_commit['avg_'+chart['code']] * prev_multiplier
            data[chart['code']] = cur - prev

        return data
