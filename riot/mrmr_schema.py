from schema_registry import *

def read_avro_schema(file_path):
    with open(file_path, 'r') as schema_file:
        avro_schema_str = schema_file.read()
    return avro_schema_str

my_file = read_avro_schema('experiment_schema.avro')

register_schema('http://localhost:8081', 'experiment', my_file)

# delete_schema('http://localhost:8081','experiment')
print(get_registered_subjects('http://localhost:8081'))

