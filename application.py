import sys
import os

# add current director to ensure these modules can be imported
sys.path.append(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

def application(environ, start_response):
    import controllers

    uri = environ["REQUEST_URI"]
    controller = controllers.route(uri)

    headers = controller.headers()
    cookies = [("Set-Cookie", morsel.OutputString()) for morsel in controller.cookie_set.values()]
    body = controller.render("container.html").encode('utf-8')

    start_response(controller.status, headers + cookies + [('Content-Length', str(len(body)))])
    return [body]
