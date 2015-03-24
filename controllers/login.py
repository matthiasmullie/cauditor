from controllers import fallback


class Controller(fallback.Controller):
    fail = False

    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "login.html"
        self.code = match.group(1)

    def match(self):
        """ matches /login?code=xyz """
        import re
        return re.match("^/login\?code=([a-f0-9]+)$", self.uri, flags=re.IGNORECASE)

    def headers(self):
        import http.cookies
        import os

        token = self.get_auth_token(self.code)
        user_id = self.import_from_github(token)

        # @todo: create session

        cookie = http.cookies.SimpleCookie()
        cookie['github_token'] = self.get_auth_token(self.code)

        # success! set cookie & redirect
        return [cookie, "Location: %s://%s/user" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"])]

    def render(self):
        if self.fail:
            return super(Controller, self).render()
        else:
            # don't render anything; we'll only be sending redirect headers
            return ""

    def import_from_github(self, token):
        import container
        import models

        github = container.github(token)
        users = models.users.Users()
        users_repos = models.users_repos.UsersRepos()

        # store user (will be updated if user with that id already exists)
        user = github.get_user()
        users.store(self.get_user(user))

        # delete existing repos & re-save all of them
        repos = [self.get_repo(repo, user) for repo in user.get_repos()]
        for org in user.get_orgs():
            repos.extend([self.get_repo(repo, user) for repo in org.get_repos()])
        users_repos.delete(user_id=user.id)
        users_repos.store(repos)

        return user.id

    def get_user(self, user):
        return {
            'id': user.id,
            'email': user.email,
            'name': user.name,
        }

    def get_repo(self, repo, user):
        return {
            'id': repo.id,
            'user_id': user.id,
            'project': repo.full_name,
            'url': repo.clone_url,
        }

    def get_auth_token(self, code):
        from urllib import parse, request
        import json

        config = self.config()

        url = 'https://github.com/login/oauth/access_token'
        values = {
            'client_id': config['github']['id'],
            'client_secret': config['github']['secret'],
            'code': code
        }
        headers = {
            'Accept': 'application/json'
        }

        data = parse.urlencode(values).encode("utf-8")
        req = request.Request(url, data, headers)
        response = request.urlopen(req)
        result = response.read().decode("utf=8")
        result = json.loads(result)

        token = result['access_token']
        scopes = result['scope'].split(",")

        # doublecheck that we have access to the scopes we need
        missing = [scope for scope in config['github']['scopes'].split(",") if scope not in scopes]
        if len(missing) > 0:
            raise Exception("Missing scopes: %s" % scopes.glue(","))

        return token
