#!/bin/bash

CONNECT_URL="http://localhost:8083"

echo "Deploying PostgreSQL source connector..."
curl -X POST $CONNECT_URL/connectors \
  -H "Content-Type: application/json" \
  -d @configs/postgres-source-connector.json

echo -e "\n\nDeploying S3 sink connector..."
curl -X POST $CONNECT_URL/connectors \
  -H "Content-Type: application/json" \
  -d @configs/s3-sink-connector.json

echo -e "\n\nChecking connector status..."
curl -X GET $CONNECT_URL/connectors
