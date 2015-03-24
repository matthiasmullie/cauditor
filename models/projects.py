from models import model


class Projects(model.DbManager):
    def __init__(self):
        super(Projects, self).__init__()
        self.table = 'projects'
