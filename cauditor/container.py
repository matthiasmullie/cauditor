import pymysql
import re
import os
import yaml


class Container:
    _environ = None
    _config = None
    _mysql = None

    def __init__(self, environ):
        self._environ = environ

    @property
    def environ(self):
        return self._environ

    @property
    def config(self):
        if self._config is None:
            # parse environment variables into config.yaml, in $VARIABLE format
            # @see http://stackoverflow.com/questions/26712003/pyyaml-parsing-of-the-environment-variable-in-the-yaml-configuration-file
            def pathex_constructor(loader, node):
                return os.environ[node.value[1:]]
            pattern = re.compile(r'\$([0-9a-z_]+)', re.IGNORECASE)
            yaml.add_implicit_resolver('tag', pattern)
            yaml.add_constructor('tag', pathex_constructor)

            path = os.path.dirname(os.path.abspath(__file__)) + '/config.yaml'
            with open(path, 'r', encoding='utf-8') as stream:
                self._config = yaml.load(stream)

        return self._config

    @property
    def mysql(self):
        if self._mysql is None:
            config = self.config['mysql']
            self._mysql = pymysql.connect(
                host=config['host'],
                user=config['user'],
                passwd=config['pass'],
                db=config['db'],
                port=int(config['port']),
                charset='utf8',
                autocommit=True
            )

        return self._mysql

    def github(self, token):
        import github
        config = self.config['github']
        return github.Github(
            login_or_token=token,
            client_id=config['id'],
            client_secret=config['secret'],
            timeout=10,
            user_agent='cauditor.org',
            per_page=999
        )
