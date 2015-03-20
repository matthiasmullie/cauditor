import pymysql


class DbManager(object):
    table = ""

    def __init__(self):
        import container
        self.__connection = container.mysql()

    def __del__(self):
        self.__connection.commit()
        self.__connection.close()

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

        # split into a list of tuple pairs; we'll be splitting
        # them apart & I want to be sure of the order of the items
        items = kwargs.items()

        # build `WHERE key = %s AND key2 = %s` clause
        where = [key + " = %s" for key, value in items]
        where = "WHERE " + " AND ".join(where)

        # gather list of params for where clause
        params = [value for key, value in items]

        # options can be a list or a string - flatten into string from here on
        options = " ".join(list(options))

        cursor = self.__connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * "
            "FROM %s " % self.table +
            where + " " +  # string of `WHERE key = %s AND key2 = %s`
            options,  # additional options (e.g. ORDER BY, LIMIT)
            params  # params for WHERE-clause
        )
        result = cursor.fetchall()
        return [self.bytes_to_string(row) for row in result]

    def store(self, data=None, **kwargs):
        """ Performs an INSERT ... ON DUPLICATE KEY UPDATE ... query

        Make sure your primary keys are fine as they'll decide over insert or update.

        Data is not validated (though a child class could implement that) so make
        sure the dict you pass is conform the schema.

        :param data: dict in {'key': 'value', 'key2': 'value2'} format
        :return: int amount of rows inserted/updated (1 or 0)
        """

        # data can come in dict form, of as parameterized kwargs
        data = data if data is not None else kwargs

        # split into a list of tuple pairs; we'll be splitting
        # them apart & I want to be sure of the order of the items
        items = data.items()

        # gather list of params for insert & update
        params = [value for key, value in items] * 2

        cursor = self.__connection.cursor()
        return cursor.execute(
            "INSERT INTO %s " % self.table +
            "(" + ", ".join([key for key, value in items]) + ") " +  # (key, key2)
            "VALUES (" + ", ".join(["%s" for key, value in items]) + ") " +  # (%s, %s)
            "ON DUPLICATE KEY UPDATE " +
            ", ".join([key + " = %s" for key, value in items]),  # key = %s, key2 = %s
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

        # split into a list of tuple pairs; we'll be splitting
        # them apart & I want to be sure of the order of the items
        items = kwargs.items()

        # build `WHERE key = %s AND key2 = %s` clause
        where = [key + " = %s" for key, value in items]
        where = "WHERE " + " AND ".join(where)

        # gather list of params for where clause
        params = [value for key, value in items]

        cursor = self.__connection.cursor()
        return cursor.execute(
            "DELETE FROM %s " % self.table +
            where,  # string of `WHERE key = %s AND key2 = %s`
            params  # params for WHERE-clause
        )

    def bytes_to_string(self, result):
        """Convert bytes-values to plain strings

        DB has some BLOB & binary fields that contain UTF-8 data.

        :param result: list[dict]
        :return: list[dict]
        """
        return {key: value.decode("utf-8") if isinstance(value, bytes) else value for key, value in result.items()}
