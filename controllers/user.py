from controllers import fallback
from github import Github


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "user.html"
        self.user = {}

    def match(self):
        """ matches /user """
        import re
        return re.match("^/user$", self.uri, flags=re.IGNORECASE)

    def args(self):
        args = super(Controller, self).args()
        args.update({
            'user': self.user,
        })
        return args

    def render(self):
        # only requesting user data here because I don't want to fall
        # to 404 if it fails; we should stay here and show login-link!
        token = self.get_auth_token()
        self.user = self.load_user(token)

        return super(Controller, self).render()

    def get_auth_token(self):
        import os
        import http.cookies

        if "HTTP_COOKIE" in os.environ:
            cookie = http.cookies.SimpleCookie()
            cookie.load(os.environ.get("HTTP_COOKIE", ""))
            if "github_token" in cookie:
                return cookie['github_token'].value

        raise Exception("No token found in cookie")

    def load_user(self, token):
        data = self.args()
        gh = Github(login_or_token=token, client_id=data["github"]["id"], client_secret=data["github"]["secret"], timeout=1, user_agent="codegraphs")
        user = gh.get_user()
        return {
            'id': user.id,
            'login': user.login,
            'name': user.name,
            'email': user.email,
            'avatar_url': user.avatar_url,
            'blog': user.blog,
            'url': user.url,
        }
