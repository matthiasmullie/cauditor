from cauditor.controllers import fallback
from cauditor.models import projects
from cauditor import listeners
from cauditor import container
import dateutil.parser
import json


class Controller(fallback.Controller):
    template = ""
    exception = ""

    def __init__(self, project, commit, branch=None):
        super(Controller, self).__init__()

        self.project = project
        self.branch = branch
        self.commit = commit

        if 'wsgi.input' in container.environ:
            try:
                request_body_size = int(container.environ.get('CONTENT_LENGTH', 0))
            except ValueError:
                request_body_size = 0

            data = container.environ['wsgi.input'].read(request_body_size)
            print(data)
            data = data.decode('utf-8')
            print(data)
        else:
            data = input()

        self.data = json.loads(data)

    def headers(self):
        headers = [('Content-Type', "application/json; charset=UTF-8")]

        try:
            if self.data['repo'].find('github.com') < 0:
                self.status = "401 Unauthorized"
                # only GitHub is supported because of potential vendor/repo collisions
                raise Exception("Only github.com repositories are currently supported.")

            project = self.get_project()
            commit = self.get_commit()

            listeners.execute(project, commit, self.data['metrics'])
        except Exception as exception:
            self.status = "401 Unauthorized"
            self.exception = exception

        return headers

    def render(self, template="container.html"):
        import json

        if self.exception:
            return json.dumps({'error': str(self.exception)})

        return json.dumps({})

    def get_project(self):
        # first check if project by that name already exists: repo url may be
        # different than the one we have in DB (ssh/https, for example)
        model = projects.Projects()
        project = model.select(name=self.project)
        try:
            return project[0]
        except Exception:
            return {
                'name': self.project,
                'git': self.data['repo'],
            }

    def get_commit(self):
        return {
            'project': self.project,
            'branch': self.branch or 'pr-'+self.data['pull-request'],
            'hash': self.commit,
            'previous': self.data['previous-commit'] or None,
            'author': self.data['author-email'],
            'timestamp': dateutil.parser.parse(self.data['timestamp']),
        }
