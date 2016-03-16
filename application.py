#!/usr/bin/env python3

import sys
import os
import http.cookies

# add current directory to ensure these modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from cauditor import controllers
from cauditor import models
from cauditor.container import Container


def application(environ, start_response):
    container = Container(environ)

    # path_info for wsgi, request_uri for cgi
    if 'PATH_INFO' in environ:
        uri = environ['PATH_INFO']
        uri = uri + '?' + environ['QUERY_STRING'] if 'QUERY_STRING' in environ else uri
    else:
        uri = environ['REQUEST_URI']

    try:
        # load existing cookies
        cookies = http.cookies.SimpleCookie(environ.get('HTTP_COOKIE', ""))

        # init session (but don't load session data yet)
        session_id = cookies['session_id'].value if 'session_id' in cookies else None
        max_age = container.config['session']['max_age']
        session = models.sessions.Model(container.mysql, session_id, max_age)

        # figure out the right controller & let it do all the pre-processing it has to
        # (e.g. validate input)
        controller = controllers.route(uri, cookies, session, container)

        headers = controller.headers()
        body = controller.render().encode('utf-8')

        # fetch new (changed) cookies & write them
        cookies = [("Set-Cookie", morsel.OutputString()) for morsel in controller.cookie_set.values()]
        # save session changes (or extend session timeout)
        session.close()

        container.mysql.close()
    except Exception as exception:
        # make sure to terminate mysql connection, also in case of request failure
        container.mysql.close()

        raise exception

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
