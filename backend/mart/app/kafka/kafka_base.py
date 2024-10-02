# kafka_base.py

from kafka import KafkaProducer, KafkaConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from google.protobuf.json_format import MessageToDict, Parse
import uuid
from settings import settings

KAFKA_BOOTSTRAP_SERVERS = [settings.KAFKA_BOOTSTRAP_SERVER] #
SCHEMA_REGISTRY_URL = settings.SCHEMA_REGISTRY_URL #http://localhost:8081

class KafkaBase:
    def __init__(self, topic, message_type):
        self.topic = topic
        self.message_type = message_type
        self.schema_registry_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY_URL})

    def generate_unique_key(self):
        return str(uuid.uuid4())

class KafkaBaseProducer(KafkaBase):
    def __init__(self, topic, message_type):
        super().__init__(topic, message_type)
        self.serializer = ProtobufSerializer(message_type, self.schema_registry_client)
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            key_serializer=str.encode,
            value_serializer=self.serializer
        )

    def send_message(self, key,  message):
        key = key or self.generate_unique_key()
        self.producer.send(self.topic, key=key, value=message)
        self.producer.flush()

class KafkaBaseConsumer(KafkaBase):
    def __init__(self, topic, message_type, group_id):
        super().__init__(topic, message_type)
        self.deserializer = ProtobufDeserializer(message_type)
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            key_deserializer=lambda x: x.decode('utf-8'),
            value_deserializer=self.deserializer
        )

    def consume_messages(self):
        for message in self.consumer:
            yield MessageToDict(message.value)