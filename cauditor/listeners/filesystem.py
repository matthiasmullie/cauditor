import subprocess
import json
import os.path
from cauditor import container


def execute(project, commit, metrics):
    config = container.load_config()

    # create path to store data file at
    path = config['data']['path'].format(pwd=os.getcwd())
    filename = config['data']['filename'].format(project=project['name'], hash=commit['hash'])
    path = path + '/' + filename
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # write file
    f = open(path, 'w')
    f.write(json.dumps(metrics))
    f.close()
