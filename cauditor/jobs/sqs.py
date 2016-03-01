import boto3
from cauditor import container


def execute(queue, message, attributes):
    config = container.load_config()

    client = boto3.client(
        service_name='sqs',
        region_name=config['s3']['region'],
        aws_access_key_id=config['aws']['access_key'],
        aws_secret_access_key=config['aws']['secret_key']
    )

    queue = client.get_queue_by_name(QueueName=queue)
    queue.send_message(
        MessageBody=message,
        MessageAttributes={key: {'StringValue': value, 'DataType': 'String'} for key, value in attributes}
    )
