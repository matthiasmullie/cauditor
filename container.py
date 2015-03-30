def load_config():
    import io
    import yaml

    stream = io.open('config.yaml', 'r')
    return yaml.load(stream)


def mysql():
    import pymysql

    config = load_config()['mysql']
    return pymysql.connect(host=config['host'], user=config['user'], passwd=config['pass'], db=config['db'], charset='utf8')


def github(token):
    import github

    config = load_config()
    return github.Github(login_or_token=token, client_id=config["github"]["id"], client_secret=config["github"]["secret"], timeout=1, user_agent="codecharts", per_page=999)
