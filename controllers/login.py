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
        import os

        try:
            token = self.get_auth_token(self.code)
            self.import_from_github(token)

            # success! set cookie & redirect
            return [self.cookie_set, "Location: %s://%s/user" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"])]
        except Exception:
            self.fail = True
            return super(Controller, self).headers()

    def render(self):
        if self.fail:
            return super(Controller, self).render()
        else:
            # don't render anything; we'll only be sending redirect headers
            return ""

    def import_from_github(self, token):
        import container

        github = container.github(token)
        user = github.get_user()

        # delete existing repos & re-save all of them
        repos = [self.get_repo(repo) for repo in user.get_repos()]
        for org in user.get_orgs():
            repos.extend([self.get_repo(repo) for repo in org.get_repos()])

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
            'name': user.name,
        }

    def get_repo(self, repo):
        return {
            'id': repo.id,
            'project': repo.full_name,
            'url': repo.clone_url,
        }

    def get_auth_token(self, code):
        from urllib import parse, request
        import json

        config = self.config()

        url = "https://github.com/login/oauth/access_token"
        values = {
            'client_id': config['github']['id'],
            'client_secret': config['github']['secret'],
            'code': code
        }
        headers = {
            'Accept': "application/json"
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
