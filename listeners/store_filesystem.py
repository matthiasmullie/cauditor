import subprocess
import json
import container
import os


# @todo: should also support submitting data elsewhere (ftp?)
def execute(project, branch, commit, data, previous):
    # @todo: don't store if it already existed... (in DB)

    config = container.load_config()

    # create path to store data file at
    path = config['data']['json_path'].format(pwd=os.getcwd(), project=project['name'], hash=commit['hash'])
    print(path)
    subprocess.call("mkdir -p $(dirname {path})".format(path=path), shell=True)

    # write file
    f = open(path, 'w')
    data = json.dumps(data)
    f.write(data)
