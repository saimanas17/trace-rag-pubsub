FROM python:3.10-slim

WORKDIR /app

COPY pubsub/pubsub_to_kafka.py .
COPY config ./config
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "pubsub_to_kafka.py"]
