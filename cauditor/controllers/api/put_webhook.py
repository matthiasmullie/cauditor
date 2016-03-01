from cauditor.controllers.api import fallback


class Controller(fallback.Controller):
    template = ""

    # hook is triggered for these events:
    # https://developer.github.com/v3/activity/events/types/#pushevent
    # https://developer.github.com/v3/activity/events/types/#pullrequestevent
    def __init__(self, project):
        super(Controller, self).__init__()

        payload = self.get_input()

        # can't examine X-Github-Event header...
        # pull_request doesn't have the 'ref' we're checking for, so that's how we can ignore that
        if not 'ref' in payload:
            return

        # only care about commits to master, no support for other branches (yet)
        if payload['ref'] != "refs/heads/master":
            return

        # create importer job
        # @todo: fire job for payload['repository']['full_name']
