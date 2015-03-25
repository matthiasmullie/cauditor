from models import model
from datetime import datetime, timedelta
import pickle


class Sessions(model.DbManager):
    """ (Ab)use model for session management """
    def __init__(self, session_id=None):
        super(Sessions, self).__init__()
        self.table = 'sessions'

        self.id = session_id or self.generate()

        # don't load data just yet, wait until we actually need it
        # ... or initialize with empty dict, if there can't be any
        self.data = {} if session_id is None else None

    def __del__(self):
        # depending on whether or not we've loaded existing data
        # already, store or extend expiration time
        self.extend() if self.data is None else self.write()

        super(Sessions, self).__del__()

    def get(self, key):
        """ Gets a value from session
        :param key: string
        :return: mixed
        """
        self.read()
        return self.data[key] if key in self.data else None

    def set(self, key, value):
        """ Stores a value in session
        :param key: string
        :param value: mixed
        """
        # we have to load the existing data because all of it is
        # serialized into 1 pickled dict when we store it again
        self.read()
        self.data[key] = value

    def read(self):
        """ Loads all session data """
        if self.data is not None:
            # already loaded
            return self.data

        self.clear_old()

        data = self.select(id=self.id)
        if len(data) == 0:
            # no existing session data
            self.data = {}
            return self.data

        if data[0]['touched'] < self.timestamp(days_ago=30):
            # check if session data hasn't yet expired (date-as-string comparison
            # here will work fine in MySQL's DATETIME format)
            self.data = {}
            return self.data

        self.data = pickle.loads(data[0]['data'])
        return self.data

    def write(self):
        """ Store all session data """
        if self.data:
            self.store({
                'id': self.id,
                'data': pickle.dumps(self.data),
                'touched': self.timestamp(),
            })

    def extend(self):
        """ Set new date for session data, prolonging its expiration time """
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE %s " % self.table +
            "SET touched = %s " +
            "WHERE id = %s",
            [self.timestamp(), self.id]
        )

    def clear_old(self):
        """ Clear old session data
        People lose their session, but the data will still be in
        DB, being completely useless until forever.
        We should clear old (expired) sessions every now and then,
        but only once in many requests is more than enough
        """
        from random import randint
        if randint(0, 999) == 0:
            return

        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM %s " % self.table +
            "WHERE touched < %s",
            [self.timestamp(days_ago=30)]
        )

    def timestamp(self, days_ago=0):
        """ Returns a MySQL DATETIME-formatted timestamp
        :param days_ago: int
        :return: string
        """
        now = datetime.now()
        expired = now - timedelta(days=days_ago)
        return expired.strftime("%Y-%m-%d %H:%M:%S")

    def generate(self):
        """Generates a session id
        :return: string
        """
        import random
        return "%032x" % random.getrandbits(128)
