from cauditor.controllers.api import fallback
from cauditor import models
from cauditor import listeners
import dateutil.parser
import dateutil.tz
import json


class Controller(fallback.Controller):
    template = ""
    exception = ""

    def headers(self):
        try:
            if self.data['repo'].find('github.com') < 0:
                self.status = "401 Unauthorized"
                # only GitHub is supported because of potential vendor/repo collisions
                raise Exception("Only github.com repositories are currently supported.")

            project = self.get_project()
            commit = self.get_commit()

            listeners.execute(
                self.container,
                project,
                commit,
                self.data['metrics'],
                self.data['avg'],
                self.data['min'],
                self.data['max'],
            )
        except Exception as exception:
            self.status = "401 Unauthorized"
            self.exception = exception

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        if self.exception:
            return json.dumps({'error': str(self.exception)})

        return json.dumps({})

    def get_project(self):
        # first check if project by that name already exists: repo url may be
        # different than the one we have in DB (ssh/https, for example)
        model = models.projects.Model(self.container.mysql)
        project = model.select(name=self.route['project'])
        try:
            return project[0]
        except Exception:
            return {
                'name': self.route['project'],
                'git': self.data['repo'],
                'default_branch': self.data['default-branch'],
            }

    def get_commit(self):
        return {
            'project': self.route['project'],
            'branch': self.route['branch'] if 'branch' in self.route else 'pr-'+self.data['pull-request'],
            'hash': self.route['commit'],
            'previous': self.data['previous-commit'] or None,
            'author': self.data['author-email'],
            'timestamp': dateutil.parser.parse(self.data['timestamp']),
        }
