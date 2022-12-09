from kafka import KafkaProducer
from datetime import datetime
import time
import json
import random
from faker import Faker
from kafka.errors import KafkaError
import numpy as np 
# pip install kafka-python

KAFKA_TOPIC_NAME_CONS = "topicA"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'kafka:9092'

if __name__ == "__main__":
    
    fake = Faker()

    kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                       value_serializer=lambda m: json.dumps(m).encode('ascii'))
    message={}
    
    while True:
            message["first_name"]= fake.name()
            message["last_name"]= fake.name()
            message["Product_name"] = fake.company_suffix()
            message["country"] = fake.country()
            message["gender"]=np.random.choice(["M", "F"], p=[0.5, 0.5])
            message["Qte"]= random.randint(1, 9)
            future = kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS,value=message)
            
            time.sleep(10)