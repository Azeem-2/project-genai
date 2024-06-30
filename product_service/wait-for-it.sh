#!/usr/bin/env bash

HOST=$1
PORT=$2
shift 2
COMMAND=$@

echo "Waiting for $HOST:$PORT to be available..."

while ! nc -z $HOST $PORT; do
  sleep 1
done

echo "$HOST:$PORT is available. Executing command."
exec $COMMAND
