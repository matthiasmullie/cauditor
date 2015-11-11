def load_environ():
    import os
    import io
    import yaml

    try:
        # for easy config: let's parse environment.yaml into os.environ
        stream = io.open('environment.yaml', 'r', encoding='utf-8')
        # force to string, like in real os.environ
        environ = {key: str(value) for key, value in yaml.load(stream).items()}
    except FileNotFoundError:
        # let's just assume config exists in env already
        environ = {}

    environ.update(os.environ)
    return environ


def load_config():
    import io
    import re
    import yaml

    # parse environment variables into config.yaml, in $VARIABLE format
    # @see http://stackoverflow.com/questions/26712003/pyyaml-parsing-of-the-environment-variable-in-the-yaml-configuration-file
    environ = load_environ()
    def pathex_constructor(loader, node):
        return environ[node.value[1:]]
    pattern = re.compile(r'\$([0-9a-z_]+)', re.IGNORECASE)
    yaml.add_implicit_resolver('tag', pattern)
    yaml.add_constructor('tag', pathex_constructor)

    stream = io.open('config.yaml', 'r', encoding='utf-8')
    return yaml.load(stream)


def mysql(**kwargs):
    import pymysql

    config = load_config()['mysql']
    return pymysql.connect(host=config['host'], user=config['user'], passwd=config['pass'], db=config['db'], port=int(config['port']), charset='utf8', **kwargs)


def github(token):
    import github

    config = load_config()['github']
    return github.Github(login_or_token=token, client_id=config['id'], client_secret=config['secret'], timeout=1, user_agent='caudit.org', per_page=999)
