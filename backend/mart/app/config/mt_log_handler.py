# Custom Kafka logging handler
import logging

from aiokafka import AIOKafkaProducer
import json
import asyncio

class KafkaLoggingHandler(logging.Handler):
    def __init__(self, producer, topic):
        logging.Handler.__init__(self)
        self.producer = producer
        self.topic = topic

    def emit(self, record):
        try:
            msg = self.format(record)
            asyncio.create_task(
                self.producer.send_and_wait(self.topic, json.dumps({'message': msg}).encode('utf-8'))
            )
        except Exception:
            self.handleError(record)