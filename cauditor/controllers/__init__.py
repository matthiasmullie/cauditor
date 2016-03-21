import re
import importlib


routes = {
    # web
    "": 'cauditor.controllers.web.fallback',  # matches anything; 404 is fallback for every request
    "^/$": 'cauditor.controllers.web.index',  # matches /
    "^/(?!api|user)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)$": 'cauditor.controllers.web.project_summary',  # matches /vendor/repo and /vendor/repo
    "^/(?!api|user)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/metrics": 'cauditor.controllers.web.project_all_metrics',  # matches /vendor/repo/overview and /vendor/repo/commit/overview
    "^/(?!api|user)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/(?P<chart>(mi|ccn|hi|i|ca|ce)+)$": 'cauditor.controllers.web.project_metrics',  # matches /vendor/repo/chart and /vendor/repo/commit/chart
    "^/(?!api|user)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/progress$": 'cauditor.controllers.web.project_all_progress',  # matches /vendor/repo/progress
    "^/(?!api|user)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/progress/(?P<chart>(mi|ccn|hi|i|ca|ce)+)$": 'cauditor.controllers.web.project_progress',  # matches /vendor/repo/progress/chart
    "^/login\?code=(?P<code>[a-f0-9]+)$": 'cauditor.controllers.web.login',  # matches /login?code=xyz
    "^/logout$": 'cauditor.controllers.web.logout',  # matches /logout
    "^/user$": 'cauditor.controllers.web.user_repos',  # matches /user
    "^/user/settings$": 'cauditor.controllers.web.user_settings',  # matches /user/settings
    "^/user/progress$": 'cauditor.controllers.web.user_all_progress',  # matches /user/progress
    "^/user/progress/(?P<chart>(mi|ccn|hi|i|ca|ce)+)$": 'cauditor.controllers.web.user_progress',  # matches /user/progress/chart
    "^/help$": 'cauditor.controllers.web.help',  # matches /help

    # api
    "^/api": 'cauditor.controllers.api.fallback',  # matches /api*; 404 fallback for every request in /api
    "^/api/user/repos$": 'cauditor.controllers.api.get_repos',  # matches /api/user/repos
    "^/api/user/settings$": 'cauditor.controllers.api.put_settings',  # matches /api/user/settings
    "^/api/user/diffs$": 'cauditor.controllers.api.get_user_commit_diffs',  # matches /api/user/diffs
    "^/api/user/link/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": 'cauditor.controllers.api.put_project',  # matches /api/link/vendor/repo
    "^/api/v1/webhook/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": 'cauditor.controllers.api.put_webhook',  # matches /api/v1/webhook/vendor/repo
    "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/((?P<branch>[a-z0-9_.-]+)/)?(?P<commit>[a-f0-9]{40})$": 'cauditor.controllers.api.put_metrics',  # matches /api/v1/vendor/repo/branch/commit
    "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/(?P<branch>[a-z0-9_.-]+)$": 'cauditor.controllers.api.get_project_commits',  # matches /api/v1/vendor/repo/branch
}


def route(uri, cookies, session, container):
    matched_controllers = {}
    for regex, controller in routes.items():
        # figure out if controller can answer uri
        match = re.match(regex, uri, flags=re.IGNORECASE)

        if match is not None:
            matched_controllers.update({controller: match})

    # sort routes based on match length (the more of a url matches, the better)
    # pick the first route (there'll always be at least 1, the fallback (404))
    matched_controllers = sorted(matched_controllers.items(), key=lambda controller: controller[1].end(0), reverse=True)

    # init controller with named args as provided by the route regex
    (module_name, match) = matched_controllers[0]
    module = importlib.import_module(module_name)

    return module.Controller(match.groupdict(), cookies, session, container)
