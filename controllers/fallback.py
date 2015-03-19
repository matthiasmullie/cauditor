class Controller(object):
    def __init__(self, uri):
        self.uri = uri
        self.template = "404.html"

    def match(self):
        """ matches anything; 404 is fallback for every request """
        import re
        return re.match("", self.uri)

    def args(self):
        return {
            # @todo: get this elsewhere; don't want this huge dict in this controller
            "graphs": [
                {
                    'code': "ccn",
                    'name': "Cyclomatic Complexity",
                    'file': "/assets/js/visualizations/treemap/CyclomaticComplexity.js",
                    'class': "Codegraphs.Visualization.Treemap.CyclomaticComplexity",
                },
                {
                    'code': "npath",
                    'name': "Npath Complexity",
                    'file': "/assets/js/visualizations/treemap/NpathComplexity.js",
                    'class': "Codegraphs.Visualization.Treemap.NpathComplexity",
                },
                {
                    'code': "wmc",
                    'name': "Weighted Metric Count",
                    'file': "/assets/js/visualizations/treemap/WeightedMetricCount.js",
                    'class': "Codegraphs.Visualization.Treemap.WeightedMetricCount",
                },
                {
                    'code': "dit",
                    'name': "Depth Inheritance Tree",
                    'file': "/assets/js/visualizations/treemap/DepthInheritanceTree.js",
                    'class': "Codegraphs.Visualization.Treemap.DepthInheritanceTree",
                },
                {
                    'code': "cr",
                    'name': "Code Rank",
                    'file': "/assets/js/visualizations/treemap/CodeRank.js",
                    'class': "Codegraphs.Visualization.Treemap.CodeRank",
                },
                {
                    'code': "ca",
                    'name': "Afferent Coupling",
                    'file': "/assets/js/visualizations/treemap/AfferentCoupling.js",
                    'class': "Codegraphs.Visualization.Treemap.AfferentCoupling",
                },
                {
                    'code': "ce",
                    'name': "Efferent Coupling",
                    'file': "/assets/js/visualizations/treemap/EfferentCoupling.js",
                    'class': "Codegraphs.Visualization.Treemap.EfferentCoupling",
                },
                {
                    'code': "i",
                    'name': "Instability",
                    'file': "/assets/js/visualizations/treemap/Instability.js",
                    'class': "Codegraphs.Visualization.Treemap.Instability",
                },
            ],
        }

    def render(self):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(self.template)
        args = self.args()
        return template.render(args)
