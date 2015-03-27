#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import controllers

uri = os.environ["REQUEST_URI"]
#uri = "/wikimedia/mediawiki-extensions-Flow"  # @todo: cli testing

matched_controllers = {}
for name in controllers.__all__:
    try:
        # attempt to construct controller from this uri
        controller = getattr(controllers, name).Controller(uri)

        # figure out length of the uri part that was matched
        matched_controllers.update({controller: controller.match().end(0)})
    except Exception:  # @todo: more specific exception class ;)
        continue

# sort routes based on match length (the more of a url matches, the better)
# pick the first route (there'll always be at least 1, the fallback (404))
controller = sorted(matched_controllers, key=matched_controllers.get, reverse=True)[0]

# add any cookies that have to be stored
if controller.cookie_set:
    print(controller.cookie_set)

# headers
for header in controller.headers():
    print(header)

print()
print(controller.render())
