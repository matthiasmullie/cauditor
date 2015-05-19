from controllers import fallback
import models


class Controller(fallback.Controller):
    template = "insight.html"

    def __init__(self):
        super(Controller, self).__init__()

        self.commits = self.load_commits() if self.settings else {}

    def args(self):
        args = super(Controller, self).args()

        args.update({
            'commits': self.commits,
            'title': args['user']['name'] if args['user'] else ''
        })
        return args

    def load_commits(self):
        model = models.commits.Commits()
        emails = self.settings['emails'].split(',')
        return model.select(author=emails, options=["ORDER BY author_date DESC", "LIMIT 5000"])
