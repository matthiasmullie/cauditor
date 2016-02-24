from cauditor.controllers import fallback
from cauditor.models import commits


class Controller(fallback.Controller):
    template = ""

    def __init__(self, project, branch):
        super(Controller, self).__init__()

        self.project = project
        self.branch = branch

    def render(self, template="container.html"):
        import json
        return json.dumps(self.get_commits())

    def get_commits(self):
        model = commits.Commits()
        imported = model.select(project=self.project, branch=self.branch)
        return [commit['hash'] for commit in imported]
