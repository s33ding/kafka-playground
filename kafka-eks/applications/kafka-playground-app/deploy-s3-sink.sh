#!/bin/bash

echo "Creating S3 Sink Connector..."

# Check if Kafka Connect is available
kubectl wait --for=condition=ready pod -l app=kafka-connect --timeout=60s

# Create the S3 sink connector
kubectl exec kafka-connect-0 -- curl -X POST \
  -H "Content-Type: application/json" \
  -d @- http://localhost:8083/connectors << 'EOF'
{
  "name": "s3-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.s3.S3SinkConnector",
    "tasks.max": "1",
    "topics": "playground-topic",
    "s3.region": "sa-east-1",
    "s3.bucket.name": "kafka-playground-sink-bucket",
    "s3.part.size": "5242880",
    "flush.size": "3",
    "storage.class": "io.confluent.connect.s3.storage.S3Storage",
    "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
    "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false"
  }
}
EOF

echo ""
echo "S3 Sink Connector created!"
echo "Check status: kubectl exec kafka-connect-0 -- curl http://localhost:8083/connectors/s3-sink-connector/status"
echo "S3 Bucket: kafka-playground-sink-bucket"
