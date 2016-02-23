from cauditor import models


class Controller(object):
    template = "404.html"

    def __init__(self):
        # init cookies
        import http.cookies
        import os
        self.cookie_data = http.cookies.SimpleCookie()
        self.cookie_data.load(os.environ.get("HTTP_COOKIE", ""))
        self.cookie_set = http.cookies.SimpleCookie()

        # all controllers extend from this one, so I'm going to special-case
        # the 404 header
        self.status = "404 Not Found" if self.__module__ == "controllers.fallback" else "200 OK"

        # init session (but don't load session data yet)
        from cauditor import models
        session_id = self.cookie('session_id')
        max_age = self.config()['session']['max_age']
        self.session_data = models.sessions.Sessions(session_id, max_age)

        self.user = self.session('user') or {}
        self.settings = {}
        if self.user:
            model = models.settings.Settings()
            settings = model.select(user=self.user['id'])
            self.settings = {entry['key']: entry['value'] for entry in settings}

    def config(self):
        from cauditor import container
        return container.load_config()

    def args(self):
        args = self.config()

        repos = self.session('repos') or []
        projects = []
        if repos:
            # get all of this user's active projects
            model = models.projects.Projects()
            repo_names = [repo['name'] for repo in repos]
            projects = model.select(name=repo_names)

        args.update({
            'controller': self.__module__,
            'template': self.template,
            'user': self.user,
            'settings': self.settings,
            'repos': repos,
            'imported_repos': [i for i in projects],
        })
        return args

    def headers(self):
        return [('Content-Type', "text/html; charset=UTF-8")]

    def render(self, template="container.html"):
        from jinja2 import Environment, FileSystemLoader
        import os
        path = os.path.dirname(os.path.abspath(__file__)) + "/../templates/"
        env = Environment(loader=FileSystemLoader(path))
        template = env.get_template(template)
        args = self.args()
        return template.render(args)

    def cookie(self, key, value=None, expire=None):
        if value is not None:
            # new cookie data to be stored
            self.cookie_set[key] = value
            if expire is not None:
                self.cookie_set[key]['max-age'] = expire

        # check if value was written to cookie in this request
        if key in self.cookie_set:
            return self.cookie_set[key].value

        # check if value already existed in cookie
        if key in self.cookie_data:
            return self.cookie_data[key].value

        return None

    def session(self, key, value=None):
        if value is not None:
            self.session_data.set(key, value)
            # make sure session_id is stored!
            max_age = self.config()['session']['max_age']
            self.cookie('session_id', self.session_data.id, max_age)

        return self.session_data.get(key)