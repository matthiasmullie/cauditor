from controllers import fallback


class Controller(fallback.Controller):
    def __init__(self, uri):
        super(Controller, self).__init__(uri)

        match = self.match()
        if match is None:
            raise Exception("Invalid route")

        self.template = "user.html"

    def match(self):
        """ matches /user """
        import re
        return re.match("^/user$", self.uri, flags=re.IGNORECASE)

    def args(self):
        token = self.get_auth_token()
        github = self.github(token)
        user = self.load_user(github)
        repos = self.load_repos(user)

        args = super(Controller, self).args()
        args.update({
            'user': {
                'id': user.id,
                'login': user.login,
                'name': user.name,
                'email': user.email,
                'avatar_url': user.avatar_url,
                'blog': user.blog,
                'url': user.url,
            },
            'repos': [{
                'id': repo.id,
                'name': repo.name,
                'clone_url': repo.clone_url,
                'private': repo.private,
                'url': repo.url,
            } for repo in repos],
        })

        return args

    def get_auth_token(self):
        import os
        import http.cookies

        if "HTTP_COOKIE" in os.environ:
            cookie = http.cookies.SimpleCookie()
            cookie.load(os.environ.get("HTTP_COOKIE", ""))
            if "github_token" in cookie:
                return cookie['github_token'].value

        raise Exception("No token found in cookie")

    def github(self, token):
        import container
        return container.github(token)

    def load_user(self, github):
        return github.get_user()

    def load_repos(self, user):
        # per_page limit is high enough - I'll only request 1 page & ignore other repos, if any
        return user.get_repos().get_page(0)
