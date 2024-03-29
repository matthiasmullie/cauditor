import pymysql
from decimal import Decimal
from datetime import datetime

class DbManager(object):
    table = ""

    def __init__(self, connection):
        self.connection = connection

    def select(self, options=None, columns=None, where=None, **kwargs):
        """ Arguments will refer to columns to be selected. E.g.: select(name="vendor/project")

        Known defects:
        * can only do equality, not >, <, >=, <=, !=, IN(), ...
        * can only do AND, not OR, no complicated structures
        * doesn't support additional cool thingies, like:
          * ORDER BY
          * LIMIT
          * JOINS
          * a whole lot more, you know

        :param options: Additional options like ORDER BY, LIMIT, ... (SQL-injection vulnerable!)
        :param columns: Specific columns to fetch (SQL-injection vulnerable!)
        :param where: Complex WHERE conditions (SQL-injection vulnerable!)
        :param kwargs: All of the WHERE conditions
        :return: iterable[dict]
        """
        select = Select(self, ['*'] if columns is None else columns)
        select.where([] if where is None else where, **kwargs)
        options = [] if options is None else options
        select.options(*options)
        return select

    def store(self, values=None, **kwargs):
        """ Performs a INSERT INTO ... ON DUPLICATE KEY ... query

        Make sure your primary keys are fine as they'll decide over insert or "update"
        (well, not really update - REPLACE first deletes, then reinserts)

        `values` is not validated (though a child class could implement that) so make
        sure the dict you pass is conform the schema.

        :param values: dict in {'key': "value", 'key2': "value2"} format, or list[dict]
        :return: int amount of rows inserted/updated
        """
        # values can come in dict form, or as parameterized kwargs
        values = values if values is not None else kwargs

        # values can also be a list of dicts (for multiple inserts) - make all of it a list now
        values = values if isinstance(values, list) else [values]

        keys = sorted(values[0])
        params = []
        # gather list of params for insert & update
        for d in values:
            params.extend([d[key] for key in keys])

        # make sure column names can't be mistaken for reserved words
        keys = ["`" + key + "`" for key in keys]

        with self.connection as cursor:
            result = cursor.execute(
                "INSERT INTO %s " % self.table +
                "(" + ", ".join(keys) + ") " +  # (`key`, `key2`)
                "VALUES (" + "), (".join([", ".join(["%s"] * len(keys))] * len(values)) + ") " +  # (%s, %s), (%s, %s)
                "ON DUPLICATE KEY UPDATE " +
                ", ".join(["%s = VALUES (%s)" % ((key,) * 2) for key in keys]),  # "`key1` = VALUES(`key1`), `key2` = VALUES(`key2`)"
                params
            )

        return result


class Select(object):
    cursor = None

    def __init__(self, parent, columns=list("*")):
        self.parent = parent  # keep parent around so its __del__ isn't run until this object is dead
        self.connection = parent.connection
        self.table = parent.table
        self.__columns = columns
        self.__where = ""
        self.__params = []
        self.__options = ""

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()

    def __iter__(self):
        """ Performs the SELECT query for the given where clause & options &
        retrieves the next item from the result list
        """
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute(
            "SELECT " + ",".join(self.__columns) + " " +
            "FROM %s " % self.table +
            self.__where + " " +
            self.__options,  # additional options (e.g. ORDER BY, LIMIT)
            self.__params
        )

        return self

    def __next__(self):
        """ Returns the next result of the SELECT query

        :return: dict
        """
        if self.cursor is None:
            self.__iter__()

        row = self.cursor.fetchone()
        if row is None:
            self.cursor.close()
            raise StopIteration

        return self.normalize(row)

    def normalize(self, row):
        result = self.bytes_to_string(row)

        # turn Decimal into float & datetime into ISO8901 string, so data can be json.dumps'ed
        for i in result:
            if isinstance(result[i], Decimal):
                result[i] = float(result[i])

            if isinstance(result[i], datetime):
                result[i] = result[i].isoformat()

        return result

    def __getitem__(self, index):
        """ Retrieve a specific item from the result list

        :param index: int
        :return: dict
        """
        # @todo index can be slice object; see http://stackoverflow.com/questions/2936863/python-implementing-slicing-in-getitem
        result = [result for i, result in enumerate(self) if i == index]

        if len(result) == 0:
            raise IndexError

        return result[0]

    def where(self, where=None, **kwargs):
        """ Set the WHERE conditions for the SELECT query

        :param where: List of (complex) WHERE conditions
        :param kwargs: All of the WHERE-conditions
        :return: self
        """
        # build `WHERE `key` IN (%s) AND `key2` IN (%s, %s)` clause
        kwargs = {key: value if isinstance(value, list) else [value] for key, value in kwargs.items()}
        where = [] if where is None else where
        for key, values in kwargs.items():
            # special case: WHERE `key` IS NULL
            if len(values) == 1 and values[0] is None:
                where.append("`" + key + "` IS NULL")
                kwargs[key] = {}
            else:
                where.append("`" + key + "` IN (" + ", ".join((["%s"] * len(values))) + ")")

        self.__where = "WHERE " + " AND ".join(where) if where else ""
        self.__params = [param for params in kwargs.values() for param in params]

        return self

    def options(self, *args):
        """ Set the options for the SELECT query

        :param args: All of the options, like ORDER BY, LIMIT, ... (SQL-injection vulnerable!)
        :return: self
        """
        options = " ".join(args)
        self.__options = options

        return self

    def update(self, values=None, **kwargs):
        """ Performs an UPDATE query on the selected rows
        E.g. .update(name="vendor/project") will set all names to "vendor/project"

        `values` is not validated (though a child class could implement that) so make
        sure the dict you pass is conform the schema.

        :param values: dict in {'key': "value", 'key2': "value2"} format, or list[dict]
        :return: int amount of rows updated
        """
        # values can come in dict form, or as parameterized kwargs
        values = values if values is not None else kwargs

        with self.connection as cursor:
            result = cursor.execute(
                "UPDATE %s " % self.table +
                "SET " + ", ".join(["`" + key + "` = %s" for key in values.keys()]) + " " +  # "SET `key1` = %s, `key2` = %s"
                self.__where,
                list(values.values()) + self.__params
            )

        return result

    def delete(self):
        """ Performs a DELETE query on the selected rows.

        :return: int amount of rows deleted
        """
        with self.connection as cursor:
            result = cursor.execute(
                "DELETE FROM %s " % self.table +
                self.__where,
                self.__params
            )

        return result

    def bytes_to_string(self, result):
        """Convert bytes-values to plain strings

        DB has some BLOB & binary fields that contain UTF-8 data.

        :param result: dict
        :return: dict
        """
        try :
            return {key: value.decode("utf-8") if isinstance(value, bytes) else value for key, value in result.items()}
        except UnicodeDecodeError:
            # pickled data, for example, will fail to decode - just fallback to original `bytes `data in that case
            return result
