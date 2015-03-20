from controllers import project


class Controller(project.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "graph.html"
        self.graph = self.load_graph(match.group(match.lastindex))
        self.project = self.load_project(match.group(1))
        self.commit = self.load_commit(match.group(1), match.group(3))

    def match(self):
        """ matches /vendor/repo/graph and /vendor/repo/commit/graph """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)(/([a-f0-9]{40}))?/([a-z]+)$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'graph': self.graph,
        })
        return args

    def load_graph(self, graph):
        args = super(Controller, self).args()

        # @todo raise exception if not found?

        # find this specific graph's data
        return [g for g in args['graphs'] if g['code'] == graph][0]
