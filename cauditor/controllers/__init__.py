import re
import importlib


routes = {
    'GET': {
        # web
        "": 'cauditor.controllers.web.fallback',  # matches anything; 404 is fallback for every request
        "^/$": 'cauditor.controllers.web.index',  # matches /
        "^/(?!api|user|help)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)$": 'cauditor.controllers.web.project_summary',  # matches /vendor/repo and /vendor/repo
        "^/(?!api|user|help)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/metrics": 'cauditor.controllers.web.project_all_metrics',  # matches /vendor/repo/overview and /vendor/repo/commit/overview
        "^/(?!api|user|help)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<commit>[a-f0-9]{40}))?/(?P<chart>(mi|ccn|npath|hi|i|ca|ce|dit)+)$": 'cauditor.controllers.web.project_metrics',  # matches /vendor/repo/chart and /vendor/repo/commit/chart
        "^/(?!api|user|help)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/progress$": 'cauditor.controllers.web.project_all_progress',  # matches /vendor/repo/progress
        "^/(?!api|user|help)(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/progress/(?P<chart>(mi|ccn|npath|hi|i|ca|ce|dit)+)$": 'cauditor.controllers.web.project_progress',  # matches /vendor/repo/progress/chart
        "^/user$": 'cauditor.controllers.web.user_repos',  # matches /user
        "^/user/login(?P<redirect>[^?]*)\?code=(?P<code>[a-f0-9]+)$": 'cauditor.controllers.web.login',  # matches /login?code=xyz
        "^/user/logout(?P<redirect>.*)$": 'cauditor.controllers.web.logout',  # matches /logout
        "^/user/settings$": 'cauditor.controllers.web.user_settings',  # matches /user/settings
        "^/user/progress$": 'cauditor.controllers.web.user_all_progress',  # matches /user/progress
        "^/user/progress/(?P<chart>(mi|ccn|npath|hi|i|ca|ce|dit)+)$": 'cauditor.controllers.web.user_progress',  # matches /user/progress/chart
        "^/user/feedback": 'cauditor.controllers.web.user_feedback',  # matches /user/feedback
        "^/help/metrics$": 'cauditor.controllers.web.help_metrics',  # matches /help/metrics
        "^/help/import$": 'cauditor.controllers.web.help_import',  # matches /help/import

        # api
        "^/api": 'cauditor.controllers.api.fallback',  # matches /api*; 404 fallback for every request in /api
        "^/api/user/repos$": 'cauditor.controllers.api.get_repos',  # matches /api/user/repos
        "^/api/user/diffs$": 'cauditor.controllers.api.get_user_commit_diffs',  # matches /api/user/diffs
        "^/api/user/colleagues": 'cauditor.controllers.api.get_colleagues',  # matches /api/user/colleagues
        "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)$": 'cauditor.controllers.api.get_project_branches',  # matches /api/v1/vendor/repo
        "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/(?P<branch>[a-z0-9_.-]+)$": 'cauditor.controllers.api.get_branch_commits',  # matches /api/v1/vendor/repo/branch
        "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/(?P<branch>[a-z0-9_.-]+)/(?P<commit>([a-f0-9]{40}|HEAD))$": 'cauditor.controllers.api.get_commit_stats',  # matches /api/v1/vendor/repo/commit
        "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)(/(?P<branch>[a-z0-9_.-]+))?/progress/(?P<chart>(mi|ccn|npath|hi|i|ca|ce|dit)+)$": 'cauditor.controllers.api.get_progress',  # matches /api/v1/vendor/repo/progress/chart
    },
    'PUT': {
        "^/api/user/settings$": 'cauditor.controllers.api.put_settings',  # matches /api/user/settings
        "^/api/user/link/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": 'cauditor.controllers.api.put_project',  # matches /api/user/link/vendor/repo
        "^/api/user/feedback": 'cauditor.controllers.api.put_feedback',  # matches /api/user/feedback
        "^/api/v1/webhook/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)": 'cauditor.controllers.api.put_webhook',  # matches /api/v1/webhook/vendor/repo
        "^/api/v1/(?P<project>[a-z0-9_.-]+/[a-z0-9_.-]+)/((?P<branch>[a-z0-9_.-]+)/)?(?P<commit>[a-f0-9]{40})$": 'cauditor.controllers.api.put_metrics',  # matches /api/v1/vendor/repo/commit & /api/v1/vendor/repo/branch/commit
    },
}


def route(method, uri, cookies, session, container):
    matched_controllers = {}
    for regex, controller in routes[method].items():
        # make sure arbitrary params are not an issue
        regex = re.sub('(\$?)$', '([\?\&].*)?\\1', regex)

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

    return module.Controller(uri, match.groupdict(), cookies, session, container)
