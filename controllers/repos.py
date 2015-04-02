from controllers import login


class Controller(login.Controller):
    template = ""

    def __init__(self):
        # we don't have (and don't need) a login code to fetch the auth
        # token, like parent does - we just want to re-use a couple of
        # parent's methods
        super(Controller, self).__init__('bogus')

    def headers(self):
        headers = ["Content-Type: application/json; charset=UTF-8"]

        try:
            token = self.session('github_token')
            self.import_from_github(token)
            self.update_changed_repos()
        except Exception:
            headers.append("Status: 401 Unauthorized")
            return headers

        return headers

    def render(self, template):
        import json
        return json.dumps(self.session('repos'))

    def update_changed_repos(self):
        """ repos (or users) can change change names, in which case we'll
        want to update the project info in our DB
        """
        import models
        model = models.projects.Projects()

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
        model.store(changed)

        # @todo: also update commits...
