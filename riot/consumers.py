from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'AMMAR',
    bootstrap_servers='localhost:9099',
    group_id='8',
    auto_offset_reset='earliest'
)
# try producer and consumer with avro
"""
to extract messages that are associated with a specific key
desired_key = 'my_key'
if statement inside the loop
that is it.
"""
for message in consumer:
    print(f'message {message.value},key {message.key}')
consumer.close()

