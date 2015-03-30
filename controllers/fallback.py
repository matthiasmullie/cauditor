class Controller(object):
    def __init__(self, uri):
        self.uri = uri
        self.template = "404.html"

        # init cookies
        import http.cookies
        import os
        self.cookie_data = http.cookies.SimpleCookie()
        self.cookie_data.load(os.environ.get("HTTP_COOKIE", ""))
        self.cookie_set = http.cookies.SimpleCookie()

        # init session (but don't load session data yet)
        import models
        session_id = self.cookie('session_id')
        max_age = self.config()['session']['max_age']
        self.session_data = models.sessions.Sessions(session_id, max_age)

    def match(self):
        """ matches anything; 404 is fallback for every request """
        import re
        return re.match("", self.uri)

    def config(self):
        import container
        return container.load_config()

    def args(self):
        args = self.config()
        args.update({
            'template': self.template,
            'user': self.session('user') or {},
            'repos': self.session('repos') or [],
        })
        return args

    def headers(self):
        return ["Content-Type: text/html; charset=UTF-8"]

    def render(self):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("codegraphs.html")
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
