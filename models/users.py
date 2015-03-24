from models import model


class Users(model.DbManager):
    def __init__(self):
        super(Users, self).__init__()
        self.table = 'users'
