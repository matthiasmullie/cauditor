from cauditor.jobs import sqs
from cauditor import container


def execute(queue, message, attributes):
    config = container.load_config()
    if queue in config['sqs'] and config['sqs'][queue]:
        sqs.execute(config['sqs'][queue], message, attributes)
