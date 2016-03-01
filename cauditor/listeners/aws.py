import boto3
import json
from cauditor import container


def execute(project, commit, metrics):
    config = container.load_config()

    client = boto3.client(
        service_name='s3',
        region_name=config['s3']['region'],
        aws_access_key_id=config['aws']['access_key'],
        aws_secret_access_key=config['aws']['secret_key']
    )

    path = config['data']['filename'].format(project=project['name'], hash=commit['hash'])

    client.put_object(
        Body=json.dumps(metrics),
        Key=path,
        ACL='public-read',
        Bucket=config['s3']['bucket'],
    )
