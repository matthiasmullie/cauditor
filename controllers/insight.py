from controllers import fallback
import models


class Controller(fallback.Controller):
    template = "insight.html"

    def __init__(self):
        super(Controller, self).__init__()

        self.commits = self.load_commits(self.user) if self.user else {}

    def args(self):
        args = super(Controller, self).args()

        args.update({
            'commits': [commit for commit in self.commits],
            'title': args['user']['name'] if args['user'] else ''
        })
        return args

    def load_commits(self, user):
        model = models.commits.Commits()
        # @todo get these emails from DB, somewhere; let users submit their emails...
        emails = user['email']
        return model.select(author=emails, options=["ORDER BY author_date DESC", "LIMIT 5000"])
