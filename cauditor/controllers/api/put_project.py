from cauditor.controllers.api import fallback
from cauditor import jobs


class Controller(fallback.Controller):
    template = ""

    def __init__(self, project):
        super(Controller, self).__init__()

        self.project = {}

    def headers(self):
        data = self.get_input()

        if "repo" not in data:
            self.status = "400 Bad Request"
            return super(Controller, self).headers()

        if "action" not in data or data["action"] not in ["link", "unlink"]:
            self.status = "400 Bad Request"
            return super(Controller, self).headers()

        try:
            self.project = self.process(data["repo"], data["action"])
        except Exception:
            self.status = "401 Unauthorized"
            return super(Controller, self).headers()

        if data["action"] == "link":
            # create importer jobs
            # import last commit
            jobs.execute('php-rest', {
                'slug': self.project['name'],
                'git': self.project['git'],
            }, 0)
            # import all missing commits
            jobs.execute('php-rest', {
                'slug': self.project['name'],
                'git': self.project['git'],
                'all': True,
            }, 300)

        return super(Controller, self).headers()

    def render(self, template="container.html"):
        import json
        return json.dumps(self.project)

    def process(self, repo, action):
        from cauditor import models

        model = models.projects.Projects()
        repo = self.get_repo(repo)

        if action == "link":
            hook = self.create_hook(repo)
            project = {
                'name': repo.full_name,
                'git': repo.clone_url,
                'github_id': repo.id,
                'github_hook': hook.id,
            }
            model.store(project)
        else:  # unlink
            results = model.select(name=repo.full_name)
            project = next(results)
            self.delete_hook(repo, project)
            results.delete()

        return project

    def get_repo(self, name):
        from cauditor import container

        token = self.session('github_token')
        github = container.github(token)

        return github.get_repo(name)

    def create_hook(self, repo):
        # https://developer.github.com/v3/repos/hooks/#create-a-hook
        return repo.create_hook(name="web", active=True, events=["push", "pull_request"], config={
            'url': "%s/api/v1/webhook/%s" % (self.config()['site']['host'], repo.full_name),
            'content_type': "json",
        })

    def delete_hook(self, repo, project):
        hook = repo.get_hook(project['github_hook'])
        hook.delete()
