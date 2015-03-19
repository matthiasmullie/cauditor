from controllers import project


class Route(project.Route):
    def __init__(self, uri):
        super(Route, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "graph.html"
        self.project = self.load_project(match.group(1))
        self.graph = self.load_graph(match.group(2))

    def match(self):
        """ matches /vendor/repo """
        import re
        return re.match("^/([a-z0-9_.-]+/[a-z0-9_.-]+)/([a-z]+)$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Route, self).args()
        args.update({
            'graph': self.graph,
        })
        return args

    def load_graph(self, graph):
        args = super(Route, self).args()

        # @todo raise exception if not found?

        # find this specific graph's data
        return [g for g in args['graphs'] if g['code'] == graph][0]
