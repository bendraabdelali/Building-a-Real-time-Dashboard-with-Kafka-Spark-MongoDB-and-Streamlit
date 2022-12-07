from kafka import KafkaProducer
from datetime import datetime
import time
from json import dumps
import random

# pip install 

KAFKA_TOPIC_NAME_CONS = "topicA"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

if __name__ == "__main__":
    kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                       value_serializer=lambda x: dumps(x).encode('utf-8'))
    message_list = []
    message = {}
    message["gender"] = "F"
    message["country"] = "Morocco"
    message["Product_name"] = "gahha"
    message["Qte"] = 3
     
    kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, message)

