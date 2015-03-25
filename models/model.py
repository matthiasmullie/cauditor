import pymysql


class DbManager(object):
    table = ""

    def __init__(self):
        import container
        self.connection = container.mysql()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def select(self, options="", **kwargs):
        """ Arguments will refer to columns to be selected. E.g.: select(name='vendor/project')

        Known defects:
        * can only do equality, not >, <, >=, <=, !=, IN(), ...
        * can only do AND, not OR, no complicated structures
        * doesn't support additional cool thingies, like:
          * ORDER BY
          * LIMIT
          * JOINS
          * a whole lot more, you know

        :param options: Additional options like ORDER BY, LIMIT, ... (SQL-injection vulnerable!)
        :param kwargs: All of the WHERE-conditions
        :return: list[dict]
        """

        # build `WHERE key IN (%s) AND key2 IN (%s, %s)` clause
        kwargs = {key: value if isinstance(value, list) else [value] for key, value in kwargs.items()}
        where = [key + " IN (" + ", ".join((["%s"] * len(values))) + ")" for key, values in kwargs.items()]
        where = "WHERE " + " AND ".join(where)

        # options can be a list or a string - flatten into string from here on
        options = " ".join(list(options))

        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * "
            "FROM %s " % self.table +
            where + " " +  # string of `WHERE key = %s AND key2 = %s`
            options,  # additional options (e.g. ORDER BY, LIMIT)
            [param for params in kwargs.values() for param in params]  # params for WHERE-clause
        )
        result = cursor.fetchall()
        return [self.bytes_to_string(row) for row in result]

    def store(self, data=None, **kwargs):
        """ Performs a REPLACE INTO query

        Make sure your primary keys are fine as they'll decide over insert or "update"
        (well, not really update - REPLACE first deletes, then reinserts)

        Data is not validated (though a child class could implement that) so make
        sure the dict you pass is conform the schema.

        :param data: dict in {'key': 'value', 'key2': 'value2'} format, or list[dict]
        :return: int amount of rows inserted/updated (1 or 0)
        """

        # data can come in dict form, of as parameterized kwargs
        data = data if data is not None else kwargs

        # data can also be a list of dicts (for multiple inserts) - make all of it a list now
        data = data if isinstance(data, list) else [data]

        keys = sorted(data[0])
        params = []
        # gather list of params for insert & update
        for d in data:
            params.extend([d[key] for key in keys])

        cursor = self.connection.cursor()
        return cursor.execute(
            "REPLACE INTO %s " % self.table +
            "(" + ", ".join(keys) + ") " +  # (key, key2)
            "VALUES (" + "), (".join([", ".join(["%s"] * len(keys))] * len(data)) + ")",  # (%s, %s), (%s, %s)
            params
        )

    def delete(self, **kwargs):
        """ Arguments will refer to columns to be deleted. E.g.: delete(name='vendor/project')

        Known defects:
        * can only do equality, not >, <, >=, <=, !=, IN(), ...
        * can only do AND, not OR, no complicated structures

        :param kwargs: All of the WHERE-conditions
        :return: int amount of rows deleted
        """

        # build `WHERE key = %s AND key2 = %s` clause
        where = [key + " = %s" for key in kwargs.keys()]
        where = "WHERE " + " AND ".join(where)

        cursor = self.connection.cursor()
        return cursor.execute(
            "DELETE FROM %s " % self.table +
            where,  # string of `WHERE key = %s AND key2 = %s`
            list(kwargs.values())  # params for WHERE-clause
        )

    def bytes_to_string(self, result):
        """Convert bytes-values to plain strings

        DB has some BLOB & binary fields that contain UTF-8 data.

        :param result: list[dict]
        :return: list[dict]
        """
        return {key: value.decode("utf-8") if isinstance(value, bytes) else value for key, value in result.items()}
