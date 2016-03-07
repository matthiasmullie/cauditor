from cauditor.controllers.api import fallback
from cauditor import models
from cauditor import jobs
import json


class Controller(fallback.Controller):
    template = ""
    project = {}

    def headers(self):
        if "repo" not in self.data:
            self.status = "400 Bad Request"
            return super(Controller, self).headers()

        if "action" not in self.data or self.data["action"] not in ["link", "unlink"]:
            self.status = "400 Bad Request"
            return super(Controller, self).headers()

        try:
            self.project = self.process(self.data["repo"], self.data["action"])
        except Exception:
            self.status = "401 Unauthorized"
            return super(Controller, self).headers()

        if self.data["action"] == "link":
            # create importer jobs
            # import last commit
            jobs.execute(self.container, 'php-rest', {
                'slug': self.project['name'],
                'git': self.project['git'],
            }, 0)
            # import all missing commits
            jobs.execute(self.container, 'php-rest', {
                'slug': self.project['name'],
                'git': self.project['git'],
                'all': True,
            }, 300)

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        return json.dumps(self.project)

    def process(self, repo, action):
        repo = self.get_repo(repo)

        model = models.projects.Model(self.container.mysql)
        results = model.select(name=repo.full_name)
        try:
            project = next(results)
        except Exception:
            # project does not yet exist in our DB
            project = None

        if action == "link" and (project is None or project['github_id'] is None):
            hook = self.create_hook(repo)

            project = {
                'name': repo.full_name,
                'git': repo.clone_url,
                'github_id': repo.id,
                'github_hook': hook.id,
            }
            model.store(project)
        elif action == "unlink" and project is not None:  # unlink
            if project['github_id'] is not None:
                self.delete_hook(repo, project)

            results.delete()

        return project

    def get_repo(self, name):
        token = self.session('github_token')
        github = self.container.github(token)

        return github.get_repo(name)

    def create_hook(self, repo):
        # https://developer.github.com/v3/repos/hooks/#create-a-hook
        return repo.create_hook(name="web", active=True, events=["push", "pull_request"], config={
            'url': "%s/api/v1/webhook/%s" % (self.container.config['site']['host'], repo.full_name),
            'content_type': "json",
        })

    def delete_hook(self, repo, project):
        hook = repo.get_hook(project['github_hook'])
        hook.delete()
