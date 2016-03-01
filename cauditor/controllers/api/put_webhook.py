from cauditor.controllers.api import fallback
from cauditor import jobs
from cauditor.models import commits

class Controller(fallback.Controller):
    template = ""

    # hook is triggered for these events:
    # https://developer.github.com/v3/activity/events/types/#pushevent
    # https://developer.github.com/v3/activity/events/types/#pullrequestevent
    def __init__(self, project):
        super(Controller, self).__init__()

        payload = self.get_input()

        # can't examine X-Github-Event header...
        # I'm going to ignore pull requests for now, by checking 'ref' (which is not present there)
        if not 'ref' in payload:
            return

        branch = payload['ref'].replace("refs/heads/")

        # import these specific commits
        # don't deliver message immediately; wait a couple of minutes and hope CI is running analyzer!
        jobs.execute('php-import-one', project['name'], {
            'git': payload['repository']['clone_url'],
            'branch': branch,
            'commits': ','.join([commit['id'] for commit in payload['commits']])
        }, 300)

        # next (only if we're on default branch), check if the commit before this push is known already,
        # otherwise we should also queue up a full analyze
        if branch == payload['repository']['default_branch']:
            model = commits.Commits()
            commit = model.select(
                project=payload['repository']['full_name'],
                branch=branch,
                hash=payload['before']
            )
            try:
                commit[0]
            except Exception:
                # import all missing commits
                jobs.execute('php-import-all', project['name'], {'git': payload['repository']['clone_url']}, 300)
