from cauditor import models
from jinja2 import Environment, FileSystemLoader
import dateutil.parser
import http.cookies
import os


class Controller(object):
    template = "404.html"
    status = "200 OK"
    uri = ""
    route = {}
    cookies = None
    cookie_set = None
    session_data = None
    container = None
    user = None
    settings = None
    template_env = None

    def __init__(self, uri, route, cookies, session, container):
        self.uri = uri
        self.route = route
        self.cookies = cookies
        self.session_data = session
        self.container = container

        self.cookie_set = http.cookies.SimpleCookie()

        # all controllers extend from this one, so I'm going to special-case
        # the 404 header
        self.status = "404 Not Found" if self.__module__ == "cauditor.controllers.web.fallback" else "200 OK"

        self.user = self.session('user') or {}
        self.settings = {}
        if self.user:
            model = models.settings.Model(self.container.mysql)
            settings = model.select(user=self.user['id'])
            self.settings = {entry['key']: entry['value'] for entry in settings}

        path = os.path.dirname(os.path.abspath(__file__)) + "/../../../templates/"
        self.template_env = Environment(loader=FileSystemLoader(path))
        self.template_env.filters['datetime'] = self.datetime

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
            'uri': self.uri,
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
        template = self.template_env.get_template(template)
        args = self.args()
        return template.render(args)

    def cookie(self, key, value=None, expire=None):
        if value is not None:
            # new cookie data to be stored
            self.cookie_set[key] = value
            self.cookie_set[key]['path'] = '/'
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

    def datetime(self, value):
        date = dateutil.parser.parse(value)
        return str(date)

    def get_score(self, commit):
        return commit['weighed_mi']

    def get_rank(self):
        scores = []
        model = models.projects.Model(self.container.mysql)
        projects = model.select(options=['ORDER BY score DESC'])
        for project in projects:
            scores.append(project['score'])

        def rank_calculator(score):
            if score is None:
                return 0

            better = 0
            for i in scores:
                if i > score:
                    better += 1
                else:
                    break

            # calculate the amount of projects that score worst than this score
            return 100 * (1 - better / len(scores) or 1)\

        return rank_calculator
