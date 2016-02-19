from cauditor.controllers import fallback
from cauditor import models
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

            if not self.commit_exists(form):
                self.store_project(form)
                self.store_commit(form)
        except Exception as exception:
            self.status = "401 Unauthorized"
            self.exception = exception

        return headers

    def render(self, template="container.html"):
        import json

        if self.exception:
            return json.dumps({'error': str(self.exception)})

        return json.dumps({})

    def commit_exists(self, form):
        project = form['slug'].value
        branch = form['branch'].value
        commit = form['commit'].value

        commits = models.commits.Commits()
        result = commits.select(project=project, branch=branch, hash=commit)

        try:
            result[0]
            return True
        except Exception:
            return False

    def store_project(self, form):
        projects = models.projects.Projects()
        project = {
            'name': form['slug'].value,
            'git': form['repo'].value,
        }
        projects.store(project)

    def store_commit(self, form):
        metrics = json.loads(form['json'].value)

        commits = models.commits.Commits()
        commit = {
            'project': form['slug'].value,
            'branch': form['branch'].value or 'pr-'+form['pull-request'].value,
            'hash': form['commit'].value,
            'previous': form['previous-commit'].value,
            'author': form['author-email'].value,
            'timestamp': dateutil.parser.parse(form['timestamp'].value),

            # metrics
            'loc': metrics['loc'],
            'noc': metrics['noc'],
            'nom': metrics['nom'],
            'ca': metrics['ca'],
            'ce': metrics['ce'],
            'i': metrics['i'],
            'dit': metrics['dit'],
            'ccn': metrics['ccn'],
            'npath': metrics['npath'],
            'he': metrics['he'],
            'hi': metrics['hi'],
            'mi': metrics['mi'],
        }
        commits.store(commit)
