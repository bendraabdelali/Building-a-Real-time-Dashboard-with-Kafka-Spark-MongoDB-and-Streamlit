from kafka import KafkaProducer
from kafka.errors import KafkaError
import csv
import json
import time
from configparser import ConfigParser

config = ConfigParser()
config.read('variables.ini')

KAFKA_TOPIC_NAME_CONS = config["KAFKA"]["KAFKA_TOPIC_NAME_CONS"]
KAFKA_BOOTSTRAP_SERVERS_CONS = config["KAFKA"]["KAFKA_BOOTSTRAP_SERVERS_CONS"]


producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS_CONS],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
def kafka_producer(data):
    try:
       future = producer.send(KAFKA_TOPIC_NAME_CONS, data)
       producer.flush()
       record_metadata = future.get(timeout=10)
       print(record_metadata)
    except KafkaError as e:
       print(e)

with open("./dataset.csv") as f:
    fdict = csv.DictReader(f, delimiter=",")
    for row in fdict:
        data = dict(row)
        kafka_producer(data)
        time.sleep(5)
        print(data)