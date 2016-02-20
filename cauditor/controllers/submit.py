from cauditor.controllers import fallback
from cauditor import listeners
import dateutil.parser
import json


class Controller(fallback.Controller):
    template = ""
    exception = ""

    def __init__(self):
        super(Controller, self).__init__()

    def headers(self):
        import cgi

        headers = [('Content-Type', "application/json; charset=UTF-8")]

        try:
            form = cgi.FieldStorage(keep_blank_values=True)

            if form['repo'].value.find('github.com') < 0:
                self.status = "401 Unauthorized"
                raise Exception("Only github.com repositories are currently supported.")

            project = self.get_project(form)
            commit = self.get_commit(form)
            metrics = self.get_metrics(form)

            listeners.execute(project, commit, metrics)
        except Exception as exception:
            self.status = "401 Unauthorized"
            self.exception = exception

        return headers

    def render(self, template="container.html"):
        import json

        if self.exception:
            return json.dumps({'error': str(self.exception)})

        return json.dumps({})

    def get_project(self, form):
        return {
            'name': form['slug'].value,
            'git': form['repo'].value,
        }

    def get_commit(self, form):
        return {
            'project': form['slug'].value,
            'branch': form['branch'].value or 'pr-'+form['pull-request'].value,
            'hash': form['commit'].value,
            'previous': form['previous-commit'].value,
            'author': form['author-email'].value,
            'timestamp': dateutil.parser.parse(form['timestamp'].value),
        }

    def get_metrics(self, form):
        return json.loads(form['json'].value)
