import logging
import json
import time
from kafka import KafkaProducer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(bootstrap_servers=["psdbdev01:9092"], value_serializer=lambda m:json.JSONEncoder().encode(m).encode('utf-8'))
for i in range(10):
    producer.send("monatest", {"hello": "world", "index": 1})
    time.sleep(1.0)


