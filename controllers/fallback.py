class Controller(object):
    def __init__(self, uri):
        self.uri = uri
        self.template = "404.html"

    def match(self):
        """ matches anything; 404 is fallback for every request """
        import re
        return re.match("", self.uri)

    def args(self):
        import container
        return container.load_config()

    def headers(self):
        return ["Content-Type: text/html"]

    def render(self):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template(self.template)
        args = self.args()
        return template.render(args)
