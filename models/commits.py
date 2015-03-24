from models import model


class Commits(model.DbManager):
    def __init__(self):
        super(Commits, self).__init__()
        self.table = 'commits'
