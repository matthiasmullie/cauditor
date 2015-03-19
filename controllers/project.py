from controllers import fallback
from models import project


class Route(fallback.Route):
    def __init__(self, uri):
        super(Route, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "project.html"
        self.project = self.load_project(match.group(1))

    def match(self):
        """ matches /vendor/repo """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Route, self).args()
        args.update({
            'project': self.project,
        })
        return args

    def load_project(self, project):
        # @todo raise exception if not found?

        return {
            # @todo; get data from DB or wherever!
            'name': project,
            'git': '',  # @todo: commit path
            'commit': "006f698169fffbac775de747661e18caa56dee83" if project == "wikimedia/mediawiki-extensions-Flow" else "temp",  # @todo: change to vendor/project/commit.json
        }
