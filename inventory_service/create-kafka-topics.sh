#!/bin/bash

# Wait for Kafka to be ready
while ! nc -z broker 9092; do   
  sleep 0.1
done

# Create the 'orders' topic
/opt/kafka/bin/kafka-topics.sh --create --topic orders --bootstrap-server broker:9092 --replication-factor 1 --partitions 1 || true
