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

        cookie = http.cookies.SimpleCookie()
        cookie['github_token'] = self.get_auth_token(self.code)

        # success! set cookie & redirect
        return [cookie, "Location: %s://%s/user" % (os.environ["REQUEST_SCHEME"], os.environ["HTTP_HOST"])]

    def render(self):
        if self.fail:
            return super(Controller, self).render()
        else:
            return ""

    def get_auth_token(self, code):
        import urllib
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

        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, data, headers)
        response = urllib.request.urlopen(req)
        result = response.read().decode("utf=8")
        result = json.loads(result)

        token = result['access_token']
        scopes = result['scope'].split(",")

        # doublecheck that we have access to the scopes we need
        missing = [scope for scope in config['github']['scopes'].split(",") if scope not in scopes]
        if len(missing) > 0:
            raise Exception("Missing scopes: %s" % scopes.glue(","))

        return token
