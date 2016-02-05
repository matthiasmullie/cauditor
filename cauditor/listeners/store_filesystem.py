import subprocess
import json
import os
from cauditor import container


def execute(project, branch, commit, data, previous):
    config = container.load_config()

    # create path to store data file at
    path = config['data']['json_path'].format(pwd=os.getcwd(), project=project['name'], hash=commit['hash'])
    subprocess.call("mkdir -p $(dirname {path})".format(path=path), shell=True)

    # write file
    f = open(path, 'w')
    data = json.dumps(data)
    f.write(data)
