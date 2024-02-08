from kafka import KafkaConsumer, TopicPartition


consumer = KafkaConsumer(
    'AMMAR',
    bootstrap_servers='localhost:9099',
    auto_offset_reset='earliest'
)

partition = TopicPartition(topic='AMMAR',partition = 0)
consumer.assign([partition])

a = 0

for message in consumer:
    print(message)
    print(message.timestamp)
    print(f'message: {message.value} from partition: {message.partition}')
    a+=1
    if a == 2:
        break

