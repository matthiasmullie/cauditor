from nose.tools import *
import controllers

def setup():
    pass

def teardown():
    pass

def test_routes():
    routes = {
        "": controllers.fallback,
        "/": controllers.index,
        "/matthiasmullie/scrapbook": controllers.project,
        "/matthiasmullie/scrapbook/019171752e7939ddd7eced6332d351c618327e53": controllers.project,
        "/matthiasmullie/scrapbook/mi": controllers.chart,
        "/matthiasmullie/scrapbook/019171752e7939ddd7eced6332d351c618327e53/mi": controllers.chart,
        "/login?code=6489faf93f05f5a6a302": controllers.login,
        "/logout": controllers.logout,
        "/user": controllers.user,
        "/insight": controllers.insight,
        "/api/link": controllers.link,
        "/api/settings": controllers.settings,
        "/api/repos": controllers.repos,

        # @todo not currently testing webhook, which will fail to init because it expects a certain payload
        #"/api/webhook": controllers.webhook,
    }

    for uri, expect in routes.items():
        controller = controllers.route(uri)
        assert controller.__class__ == expect.Controller
