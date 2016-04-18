from cauditor.controllers.api import fallback
from cauditor import models
import json


class Controller(fallback.Controller):
    colleagues=[]

    def headers(self):
        if 'id' not in self.user:
            # not logged in
            self.status = "401 Unauthorized"

            return super(Controller, self).headers()

        emails = self.settings['emails'].split(',')
        projects = self.get_projects(emails) if emails else []
        self.colleagues = self.get_colleagues(emails, projects) if projects else []

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        return json.dumps([{'project': colleague[0], 'author': colleague[1]} for colleague in self.colleagues])

    def get_projects(self, emails):
        model = models.commits.Model(self.container.mysql)
        imported = model.select(author=emails, columns=['project'], options=["GROUP BY project"])
        return [commit['project'] for commit in imported]

    def get_colleagues(self, exclude, projects):
        model = models.commits.Model(self.container.mysql)
        where = "author NOT IN ('" + "','".join(exclude) + "')"
        results = model.select(
            project=projects,
            columns=['project', 'author', 'COUNT(*) AS total'],
            where=[where],
            options=["GROUP BY project, author", "ORDER BY total DESC", "LIMIT 15"]
        )
        return [(commit['project'], commit['author']) for commit in results]
