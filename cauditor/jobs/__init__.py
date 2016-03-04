from cauditor.jobs import sqs


def execute(container, queue, message, delay=0):
    if queue in container.config['sqs']['queues'] and container.config['sqs']['queues'][queue]:
        sqs.execute(container.config, container.config['sqs']['queues'][queue], message, delay)
