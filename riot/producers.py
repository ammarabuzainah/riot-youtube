from kafka import KafkaProducer

#producer = KafkaProducer(bootstrap_servers='host.docker.internal:9092')

producer = KafkaProducer(bootstrap_servers='localhost:9099')

def read_avro_schema(file_path):

    with open(file_path, 'r') as schema_file:
        avro_schema_str = schema_file.read()
    return avro_schema_str

my_file = read_avro_schema('dummy_data.avsc')

producer.send(topic='AMMAR2', value=my_file.encode('utf-8'))

producer.flush()
producer.close()


