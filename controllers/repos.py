from controllers import login


class Controller(login.Controller):
    template = ""

    def __init__(self):
        # we don't have (and don't need) a login code to fetch the auth
        # token, like parent does - we just want to re-use a couple of
        # parent's methods
        super(Controller, self).__init__('bogus')

    def headers(self):
        headers = ["Content-Type: application/json; charset=UTF-8"]

        try:
            token = self.session('github_token')
            self.import_from_github(token)
        except Exception:
            headers.append("Status: 401 Unauthorized")
            return headers

        return headers

    def render(self, template):
        import json
        return json.dumps(self.session('repos'))
