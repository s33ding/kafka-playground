#!/bin/bash
kubectl exec kafka-connect-proper-0 -- curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "s3-sink-connector",
    "config": {
      "connector.class": "io.confluent.connect.s3.S3SinkConnector",
      "tasks.max": "1",
      "topics": "playground-topic",
      "s3.bucket.name": "s33ding-kafka-output",
      "s3.region": "sa-east-1",
      "flush.size": "3",
      "rotate.interval.ms": "60000",
      "storage.class": "io.confluent.connect.s3.storage.S3Storage",
      "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
      "partitioner.class": "io.confluent.connect.storage.partitioner.TimeBasedPartitioner",
      "partition.duration.ms": "3600000",
      "path.format": "YYYY/MM/dd/HH",
      "locale": "US",
      "timezone": "UTC"
    }
  }'
