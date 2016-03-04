from cauditor.models import model


class Model(model.DbManager):
    def __init__(self, connection):
        super(Model, self).__init__(connection)

        # yeah, this is an ugly hack :D
        self.table = 'commits INNER JOIN commit_details ON commit_id = id'

    def store(self, values=None, **kwargs):
        """ Similar to parent's store(), but altered because commit data
        lives in 2 tables: one with the commit data & one with the
        project-commit link.

        Multiple projects can have the same commit (e.g. forks), but we
        only want to store one copy.

        We'll first attempt to store the commit data. If that fails, we'll
        retrieve the existing data & link it to the new project.

        :param values: dict in {'key': "value", 'key2': "value2"} format, or list[dict]
        :return: int amount of rows inserted/updated
        """

        # values can come in dict form, or as parameterized kwargs
        values = values if values is not None else kwargs

        # values can also be a list of dicts (for multiple inserts) - make all of it a list now
        values = values if isinstance(values, list) else [values]

        with self.connection as cursor:
            row_count = 0

            for commit_details in values:
                # restructure: data is going to 2 tables
                commit = {'project': commit_details['project'], 'branch': commit_details['branch']}
                del commit_details['project'], commit_details['branch']

                # gather list of keys & params for insert & update into `commit_details`
                commit_details_keys = sorted(commit_details)
                commit_details_params = [commit_details[key] for key in commit_details_keys]

                # make sure column names can't be mistaken for reserved words
                commit_details_keys = ["`" + key + "`" for key in commit_details_keys]

                try:
                    cursor.execute(
                        "INSERT INTO commit_details" +
                        "(" + ", ".join(commit_details_keys) + ") " +  # (`key`, `key2`)
                        "VALUES (" + ", ".join(["%s"] * len(commit_details_keys)) + ")" +  # (%s, %s), (%s, %s)
                        "ON DUPLICATE KEY UPDATE " +
                        ", ".join(["%s = VALUES (%s)" % ((key,) * 2) for key in commit_details_keys]),  # "`key1` = VALUES(`key1`), `key2` = VALUES(`key2`)"
                        commit_details_params
                    )
                    commit['commit_id'] = cursor.lastrowid
                except Exception:
                    # already exists, fetch existing id
                    existing = self.select(**commit_details)[0]
                    commit['commit_id'] = existing['commit_id']

                # gather list of keys & params for insert & update into `commits`
                commit_keys = sorted(commit)
                commit_params = [commit[key] for key in commit_keys]

                try:
                    row_count += cursor.execute(
                        "INSERT INTO commits" +
                        "(" + ", ".join(commit_keys) + ") " +  # (`key`, `key2`)
                        "VALUES (" + ", ".join(["%s"] * len(commit_keys)) + ")",  # (%s, %s), (%s, %s)
                        commit_params
                    )
                except Exception:
                    # this was probably just an update...
                    pass

        return row_count
