from cauditor.controllers.web import fallback as web_fallback, index, project, chart, login, logout, user, insight
from cauditor.controllers.api import fallback as api_fallback, get_repos, put_settings, put_project, put_webhook, put_metrics, get_commits
import re


routes = {
    # web
    "": web_fallback,  # matches anything; 404 is fallback for every request
    "^/$": index,  # matches /
    "^/(?!api)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?$": project,  # matches /vendor/repo and /vendor/repo/commit
    "^/(?!api)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/(?P<chart>[a-z]+)$": chart,  # matches /vendor/repo/chart and /vendor/repo/commit/chart
    "^/login\?code=(?P<code>[a-f0-9]+)$": login,  # matches /login?code=xyz
    "^/logout$": logout,  # matches /logout
    "^/user$": user,  # matches /user
    "^/insight$": insight,  # matches /insight

    # api
    "^/api": api_fallback,  # matches /api*; 404 fallback for every request in /api
    "^/api/user/repos$": get_repos,  # matches /api/user/repos
    "^/api/user/settings$": put_settings,  # matches /api/user/settings
    "^/api/user/link/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": put_project,  # matches /api/link/vendor/repo
    "^/api/v1/webhook/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": put_webhook,  # matches /api/v1/webhook/vendor/repo
    "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/((?P<branch>[a-z0-9_.-]+)/)?(?P<commit>[a-f0-9]{40})$": put_metrics,  # matches /api/v1/vendor/repo/branch/commit
    "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/(?P<branch>[a-z0-9_.-]+)$": get_commits,  # matches /api/v1/vendor/repo/branch
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
    exceptions = []
    for i in range(0, len(matched_controllers)):
        try:
            # init controller with named args as provided by the route regex
            (controller, match) = matched_controllers[i]
            return controller.Controller(**match.groupdict())
        except Exception as exception:
            exceptions.append(exception)
            # controller failed to init - try next!
            pass

    raise Exception("No available route for uri: " + uri + '. ' + str(exceptions))
