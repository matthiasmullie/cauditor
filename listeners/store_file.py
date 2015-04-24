import subprocess
import json
import container


# @todo: should also support submitting data elsewhere (ftp?)
def execute(project, commit, data, previous):
    config = container.load_config()

    # create path to store data file at
    path = "{path}/{name}".format(path=config['analyzers']['data_path'], name=project['name'])
    subprocess.call("mkdir -p {path}".format(path=path), shell=True)

    # write file
    path = "{path}/{hash}.json".format(path=path, hash=commit['hash'])
    f = open(path, 'w')
    data = json.dumps(data)
    f.write(data)
