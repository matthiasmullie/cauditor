import io
import re
import os
import yaml


environ = dict(os.environ)
mysql_connection = None


def load_config():
    # parse environment variables into config.yaml, in $VARIABLE format
    # @see http://stackoverflow.com/questions/26712003/pyyaml-parsing-of-the-environment-variable-in-the-yaml-configuration-file
    def pathex_constructor(loader, node):
        return environ[node.value[1:]]
    pattern = re.compile(r'\$([0-9a-z_]+)', re.IGNORECASE)
    yaml.add_implicit_resolver('tag', pattern)
    yaml.add_constructor('tag', pathex_constructor)

    path = os.path.dirname(os.path.abspath(__file__)) + '/config.yaml'
    stream = io.open(path, 'r', encoding='utf-8')
    return yaml.load(stream)


def mysql():
    import pymysql

    global mysql_connection
    if mysql_connection is None:
        config = load_config()['mysql']
        mysql_connection = pymysql.connect(host=config['host'], user=config['user'], passwd=config['pass'], db=config['db'], port=int(config['port']), charset='utf8', autocommit=True)

    return mysql_connection


def github(token):
    import github

    config = load_config()['github']
    return github.Github(login_or_token=token, client_id=config['id'], client_secret=config['secret'], timeout=1, user_agent='cauditor.org', per_page=999)
