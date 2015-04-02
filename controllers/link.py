from controllers import fallback


class Controller(fallback.Controller):
    template = ""

    def __init__(self):
        super(Controller, self).__init__()
        self.project = {}

    def headers(self):
        import cgi

        headers = ["Content-Type: application/json; charset=UTF-8"]

        form = cgi.FieldStorage()
        if "repo" not in form:
            headers.append("Status: 400 Bad Request")
            return headers

        if "action" not in form or form["action"].value not in ["link", "unlink"]:
            headers.append("Status: 400 Bad Request")
            return headers

        try:
            self.project = self.process(form["repo"].value, form["action"].value)
        except Exception:
            headers.append("Status: 401 Unauthorized")
            return headers

        return headers

    def render(self, template):
        import json
        return json.dumps(self.project)

    def process(self, repo, action):
        import models

        model = models.projects.Projects()
        repo = self.get_repo(repo)

        if action == "link":
            hook = self.create_hook(repo)
            project = {
                'name': repo.full_name,
                'git': repo.clone_url,
                'hook': hook.id,
            }
            model.store(project)
        else:  # unlink
            project = model.select(name=repo.full_name)[0]
            model.delete(name=repo.full_name)
            self.delete_hook(repo, project)

        return project

    def get_repo(self, repo):
        import container

        token = self.session('github_token')
        github = container.github(token)

        return github.get_repo(repo)

    def create_hook(self, repo):
        import os

        # https://developer.github.com/v3/repos/hooks/#create-a-hook
        return repo.create_hook(name="web", active=True, events=["push", "pull_request"], config={
            'url': "%s://%s/webhook" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"]),
            'content_type': "json",
        })

    def delete_hook(self, repo, project):
        hook = repo.get_hook(project['hook'])
        hook.delete()
