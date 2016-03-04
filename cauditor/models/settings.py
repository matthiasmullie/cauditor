from cauditor.models import model


class Model(model.DbManager):
    def __init__(self, connection):
        super(Model, self).__init__(connection)
        self.table = 'settings'
