import json
import os.path


def execute(config, project, commit, metrics):
    # create path to store data file at
    path = config['data']['path'].format(pwd=os.getcwd())
    filename = config['data']['filename'].format(project=project['name'], hash=commit['hash'])
    path = path + '/' + filename
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    # write file
    with open(path, 'w') as file:
        file.write(json.dumps(metrics))
