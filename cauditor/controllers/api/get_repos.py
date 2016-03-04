from cauditor.controllers.web import login
import json


class Controller(login.Controller):
    template = ""

    def headers(self):
        headers = [('Content-Type', "application/json; charset=UTF-8")]

        try:
            token = self.session('github_token')
            self.import_from_github(token)
            self.update_changed_repos()
        except Exception:
            self.status = "401 Unauthorized"
            return headers

        return headers

    def render(self, template="container.html"):
        return json.dumps(self.session('repos'))

    def update_changed_repos(self):
        """ repos (or users) can change change names, in which case we'll
        want to update the project info in our DB
        """
        from cauditor import models
        model = models.projects.Model(self.container.mysql)

        # fetch user's repos (which were just refreshed)
        repos = self.session('repos')
        ids = [repo['id'] for repo in repos]

        # fetch all of the repos that are a project here
        projects = model.select(github_id=ids) if repos else []
        projects = {project['github_id']: project for project in projects}

        # figure out which existing projects have changed names
        changed = [repo for repo in repos if repo['id'] in projects and repo['name'] != projects[repo['id']]['name']]
        changed = [{
            'name': repo['name'],
            'git': repo['git'],
            'github_id': repo['id']
        } for repo in changed]
        if len(changed) > 0:
            model.store(changed)

        commits = models.commits.Model(self.container.mysql)
        for repo in changed:
            select = commits.select(project=projects[repo['github_id']]['name'])
            select.update(project=repo['name'])
