from cauditor.controllers.web import fallback
from cauditor import models
import requests
import json


class Controller(fallback.Controller):
    template = "login.html"

    def __init__(self, uri, route, cookies, session, container):
        super(Controller, self).__init__(uri, route, cookies, session, container)

        # we can't validate the token here yet: multiple controllers can be initialized,
        # but only 1 will be executed (though there likely won't ever be any ambiguity
        # in the URIs that would cause this one to match another controller...)
        # we'll validate the token in headers(), and will need to reuse the result in
        # render(), so we'll keep track of the status in this variable!
        self.fail = False

    def headers(self):
        try:
            token = self.get_auth_token(self.route['code'])
            self.import_from_github(token)
            self.session('github_token', token)
            self.store_email(self.session('user'))
        except Exception:
            self.fail = True
            return super(Controller, self).headers()

        # success! redirect
        self.status = "302 Found"

        # when use has not yet imported any repos, redirect them to repo-import page
        if len(self.args()['imported_repos']) == 0:
            self.route['redirect'] = '/user'

        return [('Location', "%s%s" % (self.container.config['site']['host'], self.route['redirect']))]

    def render(self, template="container.html"):
        if self.fail:
            return super(Controller, self).render(template)
        else:
            # don't render anything; we'll only be sending redirect headers
            return ""

    def import_from_github(self, token):
        github = self.container.github(token)
        user = github.get_user()

        # delete existing repos & re-save all of them
        repos = [self.get_repo(repo) for repo in user.get_repos()]

        # I only want to store this as session data - there's no point in storing it
        # in a proper `user` table since:
        # * GitHub is the real source of the data and we need to refresh it every login
        # * if session expires, we have to re-login (using GitHub) anyway
        # might as well not be tied to any schema if there's no benefit...
        self.session('user', self.get_user(user))
        self.session('repos', repos)

        return user.id

    def get_user(self, user):
        return {
            'id': user.id,
            'email': user.email,
            'username': user.login,
            'name': user.name,
            'avatar': user.avatar_url,
        }

    def get_repo(self, repo):
        return {
            'id': repo.id,
            'name': repo.full_name,
            'url': repo.html_url,
            'git': repo.clone_url,
            'private': repo.private,
            'language': repo.language,
            'fork': repo.fork,
            'forks_count': repo.forks_count,
            # 'subscribers_count': repo.subscribers_count,  # doesn't yet exist in this version of pygithub
            'stargazers_count': repo.stargazers_count,
        }

    def get_auth_token(self, code):
        config = self.container.config

        url = "https://github.com/login/oauth/access_token"
        values = {
            'client_id': config['github']['id'],
            'client_secret': config['github']['secret'],
            'code': code
        }
        headers = {
            'Accept': "application/json"
        }

        response = requests.get(url, data=values, headers=headers)
        result = json.loads(response.text)

        token = result['access_token']
        scopes = result['scope'].split(",")

        # doublecheck that we have access to the scopes we need
        missing = [scope for scope in config['github']['scopes'].split(",") if scope not in scopes]
        if len(missing) > 0:
            raise Exception("Missing scopes: %s" % scopes.glue(","))

        return token

    def store_email(self, user):
        # figure out if any email address has already been stored
        model = models.settings.Model(self.container.mysql)
        try:
            data = model.select(user=user['id'], key="emails")
            store = data[0]["value"] == ""
        except Exception:
            # trying to access [0] will have fail if it didn't exist
            store = True

        # store user email if it doesn't already exist
        if store:
            model = models.settings.Model(self.container.mysql)
            model.store({
                'user': user['id'],
                'key': 'emails',
                'value': user['email'] if user['email'] else '',
            })
