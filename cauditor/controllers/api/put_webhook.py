from cauditor.controllers.api import fallback
from cauditor import models
from cauditor import jobs


class Controller(fallback.Controller):
    # hook is triggered for these events:
    # https://developer.github.com/v3/activity/events/types/#pushevent
    # https://developer.github.com/v3/activity/events/types/#pullrequestevent
    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        # can't examine X-Github-Event header...
        # I'm going to ignore pull requests for now, by checking 'ref' (which is not present there)
        if 'ref' not in self.data:
            return

        branch = self.data['ref'].replace("refs/heads/", '')

        # import these specific commits
        # don't deliver message immediately; wait a couple of minutes and hope CI is running analyzer!
        jobs.execute(self.container, 'php-priority', {
            'slug': self.route['project'],
            'git': self.data['repository']['clone_url'],
            'branch': branch,
            'commits': ','.join([commit['id'] for commit in self.data['commits']]),
        }, 300)

        # next (only if we're on default branch), check if the commit before this push is known already,
        # otherwise we should also queue up a full analyze
        if branch == self.data['repository']['default_branch']:
            model = models.commits.Model(self.container.mysql)
            commit = model.select(
                project=self.data['repository']['full_name'],
                branch=branch,
                hash=self.data['before']
            )
            try:
                commit[0]
            except Exception:
                # import all missing commits
                jobs.execute(self.container, 'php-rest', {
                    'slug': self.route['project'],
                    'git': self.data['repository']['clone_url'],
                    'all': True,
                }, 300)
