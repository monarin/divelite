import logging
import json
import time
from kafka import KafkaProducer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bootstrap_server = "testfac-lgbkdb:9092"
#bootstrap_server = "psdbdev01:9092"
producer = KafkaProducer(bootstrap_servers=[bootstrap_server], value_serializer=lambda m:json.JSONEncoder().encode(m).encode('utf-8'))
for i in range(10):
    producer.send("monatest", {"hello": "world", "index": 1})
    time.sleep(1.0)


