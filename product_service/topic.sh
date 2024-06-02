#!/bin/bash

# Wait until Kafka broker is ready
while ! nc -z broker 19092; do   
  sleep 1
done

# Create Kafka topic
kafka-topics.sh --create --topic product-registered --bootstrap-server broker:19092 --partitions 1 --replication-factor 1
