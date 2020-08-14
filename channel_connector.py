# coding: utf-8
import logging

import pika
from threading import Thread

logger = logging.getLogger("daemon_log")


class ChannelConnector(Thread):

    def __init__(self, queue):
        super(ChannelConnector, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            self.connect(**self.queue.get())

    def connect(self, server, login, password, queue, handler):
        try:
            file_name, klass_name = handler.split(".")
            module = __import__("services.%s" % file_name, fromlist=[file_name])
            klass = getattr(module, klass_name)

            if not klass:
                raise AttributeError("get class %s", klass_name)

            handlers = klass()

            handle = getattr(handlers, "handle")
            if not handle:
                raise AttributeError("method handle not found in %s" % klass.__name__)

            def callback(ch, method, properties, body):
                try:
                    logger.info("queue %s got data" % queue)
                    handle(body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    logger.error(e.message)

            credentials = pika.PlainCredentials(login, password)
            parameters = pika.ConnectionParameters(
                server["addr"], server["port"], server["path"], credentials
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue, durable=True)

            channel.basic_consume(queue, callback, auto_ack=False)
            channel.start_consuming()

        except (ImportError, AttributeError) as e:
            logger.error(e.message)
            self.queue.task_done()

    def stop(self):
        self.queue.task_done()