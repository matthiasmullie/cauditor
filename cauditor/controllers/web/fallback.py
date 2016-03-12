from cauditor import models
from jinja2 import Environment, FileSystemLoader
import http.cookies
import os


class Controller(object):
    template = "404.html"
    status = "200 OK"
    route = {}
    cookies = http.cookies.SimpleCookie()
    session_data = None
    container = None
    cookie_set = http.cookies.SimpleCookie()
    user = None
    settings = None

    def __init__(self, route, cookies, session, container):
        self.route = route
        self.cookies = cookies
        self.session_data = session
        self.container = container

        # all controllers extend from this one, so I'm going to special-case
        # the 404 header
        self.status = "404 Not Found" if self.__module__ == "cauditor.controllers.web.fallback" else "200 OK"

        self.user = self.session('user') or {}
        self.settings = {}
        if self.user:
            model = models.settings.Model(self.container.mysql)
            settings = model.select(user=self.user['id'])
            self.settings = {entry['key']: entry['value'] for entry in settings}

    def args(self):
        args = self.container.config

        repos = self.session('repos') or []
        projects = []
        if repos:
            # get all of this user's active projects
            model = models.projects.Model(self.container.mysql)
            repo_names = [repo['name'] for repo in repos]
            projects = model.select(name=repo_names)

        args.update({
            'controller': self.__module__,
            'template': self.template,
            'route': self.route,
            'user': self.user,
            'settings': self.settings,
            'repos': repos,
            'imported_repos': [i for i in projects if i['github_id'] is not None],
        })
        return args

    def headers(self):
        return [('Content-Type', "text/html; charset=UTF-8")]

    def render(self, template="container.html"):
        path = os.path.dirname(os.path.abspath(__file__)) + "/../../templates/"
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
        if key in self.cookies:
            return self.cookies[key].value

        return None

    def session(self, key, value=None):
        if value is not None:
            self.session_data.set(key, value)
            # make sure session_id is stored!
            max_age = self.container.config['session']['max_age']
            self.cookie('session_id', self.session_data.id, max_age)

        return self.session_data.get(key)
