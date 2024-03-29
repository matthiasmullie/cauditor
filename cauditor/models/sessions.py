from cauditor.models import model
from datetime import datetime, timedelta
from random import randint, getrandbits
import dateutil.parser
import json


class Model(model.DbManager):
    id = None
    data = None

    """ (Ab)use model for session management """
    def __init__(self, connection, session_id=None, max_age=None):
        super(Model, self).__init__(connection)

        self.table = 'sessions'

        self.id = session_id or self.generate()

        # session expiration is actually handled by the cookie (which will
        # be killed after its max_age), but since we're storing the data
        # on the server, we want to discard it at some point if it's no
        # longer valid
        # if no max_age was specified, default to storing date for 30 days
        # without max_age, the cookie will likely have expired by then
        # (when browser closes) and data is safe to be deleted
        self.max_age = max_age or 30 * 60 * 60 * 24

        # don't load data just yet, wait until we actually need it
        # ... or initialize with empty dict, if there can't be any
        if session_id is None:
            self.data = {}

    def close(self):
        # depending on whether or not we've loaded existing data
        # already, store or extend expiration time
        # this is not __del__ because apparently, destruction order can be
        # odd & connection can be
        self.extend() if self.data is None else self.write()

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
        # serialized into 1 json'ed dict when we store it again
        self.read()
        self.data[key] = value

    def read(self):
        """ Loads all session data """
        if self.data is not None:
            # already loaded
            return self.data

        self.clear_old()

        data = self.select(id=self.id)
        try:
            data = data[0]
            data['touched'] = dateutil.parser.parse(data['touched'])
        except IndexError:
            # no existing session data
            self.data = {}
            return self.data

        if data['touched'] < self.timestamp(seconds_ago=self.max_age):
            # check if session data hasn't yet expired
            self.data = {}
            return self.data

        self.data = json.loads(data['data'])
        return self.data

    def write(self):
        """ Store all session data """
        if self.data:
            self.store({
                'id': self.id,
                'data': json.dumps(self.data),
                'touched': self.timestamp(),
            })

    def extend(self):
        """ Set new date for session data, prolonging its expiration time """
        with self.connection as cursor:
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
        if randint(0, 999) != 0:
            return

        with self.connection as cursor:
            cursor.execute(
                "DELETE FROM %s " % self.table +
                "WHERE touched < %s",
                [self.timestamp(seconds_ago=self.max_age)]
            )

    def timestamp(self, seconds_ago=0):
        """ Returns a timestamp of a certain amount of days ago
        :param days_ago: int
        :return: string
        """
        now = datetime.now()
        return now - timedelta(seconds=seconds_ago)

    def generate(self):
        """Generates a session id
        :return: string
        """
        return "%032x" % getrandbits(128)
