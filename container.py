def load_config():
    import io
    import yaml

    stream = io.open('config.yaml', 'r')
    return yaml.load(stream)


def mysql():
    import pymysql

    config = load_config()['mysql']
    return pymysql.connect(host=config['host'], user=config['user'], passwd=config['pass'], db=config['db'], charset='utf8')
