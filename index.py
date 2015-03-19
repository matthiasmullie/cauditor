#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import os
import controllers

uri = os.environ["REQUEST_URI"]
#uri = "/wikimedia/mediawiki-extensions-Flow"  # @todo: cli testing

matched_routes = {}
for name in controllers.__all__:
    try:
        # attempt to construct route from this uri
        route = getattr(controllers, name).Route(uri)

        # figure out length of the uri part that was matched
        matched_routes.update({route: route.match().end(0)})
    except Exception:  # @todo: more specific exception class ;)
        continue

# sort routes based on match length (the more of a url matches, the better)
# pick the first route (there'll always be at least 1, the fallback (404))
controller = sorted(matched_routes, key=matched_routes.get, reverse=True)[0]

# headers
print("Content-Type: text/html")
print()

print(controller.render())
