import logging
from kafka import KafkaConsumer
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
bootstrap_server = "testfac-lgbkdb:9092"
#bootstrap_server = "psdbdev01:9092"
#consumer = KafkaConsumer(bootstrap_servers=["psdbdev01:9092"], group_id="monatest", max_poll_interval_ms=500000, max_poll_records=50)
consumer = KafkaConsumer(bootstrap_servers=[bootstrap_server], max_poll_interval_ms=500000, max_poll_records=50)
consumer.topics()
consumer.subscribe(["monatest"])
for msg in consumer:
    try:
        logger.info("Message from Kafka %s", msg)
        info = json.loads(msg.value)
        logger.info("JSON from Kafka %s", info)
        message_type = msg.topic
        print("Do your processing here")
    except Exception as e:
        logger.exception("Exception processing Kafka message.")

