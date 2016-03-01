from cauditor.jobs import sqs
from cauditor import container


def execute(queue, message, attributes):
    config = container.load_config()
    if queue in config['sqs']['queues'] and config['sqs']['queues'][queue]:
        sqs.execute(config['sqs']['queues'][queue], message, attributes)
