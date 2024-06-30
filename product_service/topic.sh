#!/bin/bash
# Install netcat if not already installed
if ! command -v nc &> /dev/null; then
    echo "netcat not found, installing..."
    apt-get update && apt-get install -y netcat-openbsd
fi

# Wait until Kafka broker is ready
while ! nc -z broker 19092; do
    echo "Waiting for Kafka broker to be ready..."
    sleep 1
done

# Create Kafka topic
kafka-topics.sh --create --topic product-registered --bootstrap-server broker:19092 --partitions 1 --replication-factor 1 || {
    echo "Failed to create topic 'product-registered'"
}
