#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import controllers

uri = os.environ["REQUEST_URI"]
#uri = "/wikimedia/mediawiki-extensions-Flow"  # @todo: cli testing

controller = controllers.route(uri)

# headers
headers = controller.headers()
if controller.cookie_set:
    print(controller.cookie_set)
for header in headers:
    print(header)

print()
print(controller.render("container.html"))
