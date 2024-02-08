import requests
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
import json
from schema_registry import get_schema_from_schema_registry

with open('sample_data.json', 'r') as file:
    json_data = json.load(file)

print(type(json_data))

# def avro_producer(kafka_url, schema_registry_url, schema_registry_subject):
#     # schema registry
#     sr, latest_version = get_schema_from_schema_registry(schema_registry_url, schema_registry_subject)
#
#
#     value_avro_serializer = AvroSerializer(schema_registry_client = sr,
#                                           schema_str = latest_version.schema.schema_str,
#                                           conf={
#                                               'auto.register.schemas': False
#                                             }
#                                           )
#
#     # Kafka Producer
#     producer = SerializingProducer({
#         'bootstrap.servers': kafka_url,
#         'security.protocol': 'plaintext',
#         'value.serializer': value_avro_serializer,
#         'delivery.timeout.ms': 120000,
#         'enable.idempotence': 'true'
#     })
#
#     return producer
#
# producer = avro_producer('localhost:9099', 'http://localhost:8081', 'winston')
#
# # do not convert json_data to a string; pass it directly as a dictionary
# producer.produce(topic='winston', value=json_data)
#
# producer.flush()