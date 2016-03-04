#!/usr/bin/env python3

import sys
import os
import http.cookies
from cauditor import controllers
from cauditor import models
from cauditor.container import Container

# add current directory to ensure these modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def application(environ, start_response):
    uri = environ["REQUEST_URI"]
    container = Container(environ)

    # load existing cookies
    cookies = http.cookies.SimpleCookie()
    cookies.load(container.environ.get("HTTP_COOKIE", ""))

    # init session (but don't load session data yet)
    session_id = cookies['session_id'].value if 'session_id' in cookies else None
    max_age = container.config['session']['max_age']
    session = models.sessions.Model(container.mysql, session_id, max_age)

    # figure out the right controller & let it do all the pre-processing it has to
    # (e.g. validate input)
    controller = controllers.route(uri, cookies, session, container)

    headers = controller.headers()
    # fetch new (changed) cookies & write them
    cookies = [("Set-Cookie", morsel.OutputString()) for morsel in controller.cookie_set.values()]
    body = controller.render().encode('utf-8')

    start_response(controller.status, headers + cookies + [('Content-Length', str(len(body)))])
    return [body]


if __name__ == '__main__':
    # this will wrap around above mod_wsgi-compatible code to
    # respond to cgi-script requests
    def start_response(status, headers):
        print("Status: " + status)
        print("\n".join([key + ": " + value for key, value in headers]))
        print()

    body = application(os.environ, start_response)[0]
    print(body.decode('utf-8'))
