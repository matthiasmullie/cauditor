#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import controllers

# for easy config: let's parse environment.yaml into os.environ
try:
    import io
    import yaml
    stream = io.open('environment.yaml', 'r', encoding='utf-8')
    environ = yaml.load(stream)
    for i in environ:
        os.environ[i] = str(environ[i])
except FileNotFoundError:
    # let's just assume config exists in env already
    pass

uri = os.environ["REQUEST_URI"]
controller = controllers.route(uri)

# headers
headers = controller.headers()
if controller.cookie_set:
    print(controller.cookie_set)
for header in headers:
    print(header)

print()
print(controller.render("container.html"))
