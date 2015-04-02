from controllers import fallback, index, project, chart, login, logout, user, link, repos, webhook
import re


routes = {
    "": fallback,  # matches anything; 404 is fallback for every request
    "^/$": index,  # matches /
    "^/(?!api)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?$": project,  # matches /vendor/repo and /vendor/repo/commit
    "^/(?!api)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/(?P<chart>[a-z]+)$": chart,  # matches /vendor/repo/chart and /vendor/repo/commit/chart
    "^/login\?code=(?P<code>[a-f0-9]+)$": login,  # matches /login?code=xyz
    "^/logout$": logout,  # matches /logout
    "^/user$": user,  # matches /user
    "^/api/link": link,  # matches /api/link
    "^/api/repos$": repos,  # matches /api/repos
    "^/api/webhook": webhook,  # matches /api/webhook
}


def route(uri):
    matched_controllers = {}
    for regex, controller in routes.items():
        # figure out if controller can answer uri
        match = re.match(regex, uri, flags=re.IGNORECASE)

        if match is not None:
            matched_controllers.update({controller: match})

    # sort routes based on match length (the more of a url matches, the better)
    # pick the first route (there'll always be at least 1, the fallback (404))
    matched_controllers = sorted(matched_controllers.items(), key=lambda controller: controller[1].end(0), reverse=True)
    for i in range(0, len(matched_controllers)):
        try:
            # init controller with named args as provided by the route regex
            (controller, match) = matched_controllers[i]
            return controller.Controller(**match.groupdict())
        except Exception:
            # controller failed to init - try next!
            pass

    raise Exception("No available route")
