from cauditor.controllers import fallback
from cauditor import container
from cauditor import models
from cauditor import importers
import sys
import json


class Controller(fallback.Controller):
    template = ""

    # hook is triggered for these events:
    # https://developer.github.com/v3/activity/events/types/#pushevent
    # https://developer.github.com/v3/activity/events/types/#pullrequestevent
    def __init__(self):
        super(Controller, self).__init__()

        length = int(container.environ['CONTENT_LENGTH'])
        data = sys.stdin.read(length)
        payload = json.loads(data)

        # can't examine X-Github-Event header...
        # pull_request doesn't have the 'ref' we're checking for, so that's how we can ignore that
        if not 'ref' in payload:
            return

        # only care about commits to master, no support for other branches (yet)
        if payload['ref'] != "refs/heads/master":
            return

        # create importer job
        jobs = models.jobs.Jobs()
        jobs.add(importers.since_last_commit.Importer(payload['repository']['full_name']))
