
from kafka import KafkaProducer

def read_avro_schema(file_path):
    with open(file_path, 'r') as schema_file:
        avro_schema_str = schema_file.read()
    return avro_schema_str

my_file = read_avro_schema('mrmr.avro')

print(type(my_file))

# producer = KafkaProducer(bootstrap_servers='localhost:9099')

# for line in my_file:
#     print(line)
#     producer.send(topic='AMMAR', value=line)