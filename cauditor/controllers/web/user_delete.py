from cauditor import models
from cauditor.controllers.web import user
import requests

class Controller(user.Controller):
    def headers(self):
        token = self.session('github_token')

        # make sure user is logged in...
        if token != None:
            # delete user settings
            self.delete_user_settings(self.session('user')['id'])

            # remove all repos & their hooks
            repos = [repo['name'] for repo in self.session('repos')]
            self.delete_projects(repos, token)

            # revoke current token
            self.revoke_authorization(token)

            # expire session cookie
            self.cookie('session_id', self.session_data.id, -1)

        # redirect to homepage
        self.status = "302 Found"
        return [('Location', "%s" % (self.container.config['site']['host']))]

    def render(self, template="container.html"):
        # don't render anything; we'll only be sending redirect headers
        return ""

    def delete_user_settings(self, user_id):
        model = models.settings.Model(self.container.mysql)

        results = model.select(user=user_id)
        results.delete()

    def delete_projects(self, repos, token):
        github = self.container.github(token)

        model = models.projects.Model(self.container.mysql)
        projects = model.select(name=repos, where=["github_hook IS NOT NULL"])
        for project in projects:
            repo = github.get_repo(project['name'])
            hook = repo.get_hook(project['github_hook'])
            hook.delete()

        projects.delete()

    def revoke_authorization(self, token):
        config = self.container.config
        client_id = config['github']['id']
        client_secret = config['github']['secret']

        # https://developer.github.com/v3/oauth_authorizations/#revoke-an-authorization-for-an-application
        # DELETE /applications/:client_id/tokens/:access_token
        url = "https://api.github.com/applications/%s/tokens/%s" % (client_id, token)
        response = requests.delete(url, auth=requests.auth.HTTPBasicAuth(client_id, client_secret))

