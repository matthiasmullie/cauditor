from models import model


class UsersRepos(model.DbManager):
    def __init__(self):
        super(UsersRepos, self).__init__()
        self.table = 'users_repos'
