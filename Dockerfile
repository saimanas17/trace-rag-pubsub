FROM python:3.10-slim

WORKDIR /app

COPY pubsub_to_kafka.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "pubsub_to_kafka.py"]
