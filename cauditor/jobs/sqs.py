import boto3
from cauditor import container


def execute(queue, message, attributes, delay=0):
    config = container.load_config()

    sqs = boto3.resource(
        service_name='sqs',
        region_name=config['s3']['region'],
        aws_access_key_id=config['aws']['access_key'],
        aws_secret_access_key=config['aws']['secret_key']
    )

    queue = sqs.get_queue_by_name(QueueName=queue)
    queue.send_message(
        MessageBody=message,
        MessageAttributes={key: {'StringValue': value, 'DataType': 'String'} for key, value in attributes.items()},
        DelaySeconds=delay,
    )
