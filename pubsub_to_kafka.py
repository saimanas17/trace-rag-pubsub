import json
import os
import logging
import sys
import traceback
from google.cloud import pubsub_v1
from kafka import KafkaProducer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('pubsub-to-kafka')

# Log startup information
logger.info("🚀 Starting pubsub-to-kafka service")

try:
    # GCP Pub/Sub setup
    project_id = "csye7125-dev-449823"
    subscription_id = "gcs-subscription"

    # Initialize the Pub/Sub subscriber client
    logger.info(f"Initializing Pub/Sub client for project {project_id}")
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    logger.info(f"Using subscription path: {subscription_path}")

    # Kafka setup
    logger.info("Initializing Kafka producer")
    producer = KafkaProducer(
        bootstrap_servers=["kafka:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    kafka_topic = "gcs-topic"
    logger.info(f"Kafka producer initialized, will send to topic: {kafka_topic}")


    def callback(message):
        try:
            logger.info("📨 Received a message from Pub/Sub")
            data = json.loads(message.data.decode("utf-8"))
            logger.info(f"🔍 Message data: {data}")

            if 'name' in data and data.get("contentType", "") == "application/pdf":
                payload = {
                    "bucket": data.get("bucket", ""),
                    "file": data.get("name", ""),
                    "eventType": data.get("eventType", "OBJECT_FINALIZE"),
                    "source": "pubsub-trigger",
                    "triggered_by": "gcs-upload"
                }
                producer.send(kafka_topic, value=payload)
                logger.info(f"✅ Sent to Kafka: {payload}")
            else:
                logger.warning(f"⚠️ Skipped non-PDF or invalid event: {data}")

            message.ack()
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            # You might want to nack the message here depending on your error handling strategy
            message.ack()  # Still ack to prevent infinite retries


    # Add a heartbeat to confirm the service is still running
    import threading
    import time


    def log_heartbeat():
        while True:
            logger.info("💓 Heartbeat: Still running and listening for Pub/Sub messages")
            time.sleep(60)  # Log every minute


    heartbeat_thread = threading.Thread(target=log_heartbeat, daemon=True)
    heartbeat_thread.start()

    # Start listening for messages
    logger.info(f"🔁 Listening for GCS → Pub/Sub events on: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    # Keep the main thread alive
    try:
        logger.info("Main thread waiting for messages...")
        streaming_pull_future.result()  # Block until the future completes
    except KeyboardInterrupt:
        logger.info("👋 Received interrupt, shutting down...")
        streaming_pull_future.cancel()

except Exception as e:
    logger.error(f"💥 Fatal error in Pub/Sub subscriber: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)