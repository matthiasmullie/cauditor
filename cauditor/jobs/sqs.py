import boto3
import json


def execute(config, queue, message, delay=0):
    sqs = boto3.resource(
        service_name='sqs',
        region_name=config['sqs']['region'],
        aws_access_key_id=config['aws']['access_key'],
        aws_secret_access_key=config['aws']['secret_key']
    )

    queue = sqs.get_queue_by_name(QueueName=queue)
    queue.send_message(
        MessageBody=json.dumps(message),
        DelaySeconds=delay,
    )
