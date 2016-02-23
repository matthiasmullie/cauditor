import boto3
import json
import os.path
from cauditor import container


def execute(project, commit, metrics):
    config = container.load_config()

    s3 = boto3.resource(
        service_name='s3',
        aws_access_key_id=config['s3']['access_key'],
        aws_secret_access_key=config['s3']['secret_key'],
    )

    path = config['data']['path'].format(pwd='', project=project['name'], hash=commit['hash'])
    path = os.path.basename(path)

    file = s3.Object(config['s3']['bucket'], path)
    file.put(Body=json.dumps(metrics), ACL='public-read')