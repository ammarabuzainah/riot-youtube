from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry import Schema

schema_registry_url = 'http://schema-registry:8081'
# schema_registry_url = 'http://localhost:8081'

def get_schema_from_schema_registry(schema_registry_url, kafka_topic):
    schema_registry_subject = f"{kafka_topic}-value"
    sr = SchemaRegistryClient({'url': schema_registry_url})
    latest_version = sr.get_latest_version(schema_registry_subject)
    return sr, latest_version


def register_schema(schema_registry_url, kafka_topic, schema_str):
    schema_registry_subject = f"{kafka_topic}-value"
    sr = SchemaRegistryClient({'url': schema_registry_url})
    schema = Schema(schema_str, schema_type="AVRO")
    schema_id = sr.register_schema(subject_name=schema_registry_subject, schema=schema)

    return schema_id


def update_schema(schema_registry_url, kafka_topic, schema_str):
    schema_registry_subject = f"{kafka_topic}-value"
    sr = SchemaRegistryClient({'url': schema_registry_url})
    versions_deleted_list = sr.delete_subject(schema_registry_subject, permanent=True)
    print(f"versions of schema deleted list: {versions_deleted_list}")

    schema_id = register_schema(schema_registry_url, schema_registry_subject, schema_str)
    return schema_id


def get_registered_subjects(schema_registry_url):
    sr = SchemaRegistryClient({'url': schema_registry_url})
    subjects = sr.get_subjects()

    return subjects


def delete_schema(schema_registry_url,kafka_topic):
    schema_registry_subject = f"{kafka_topic}-value"
    sr = SchemaRegistryClient({'url': schema_registry_url})
    versions_deleted_list = sr.delete_subject(schema_registry_subject, permanent=True)
    return f"successfully deleted schema of {kafka_topic} version of {versions_deleted_list}"

