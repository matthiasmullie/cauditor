from cauditor.models import model


class Settings(model.DbManager):
    def __init__(self):
        super(Settings, self).__init__()
        self.table = 'settings'
