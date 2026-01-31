#!/bin/bash
set -e

echo "🔗 Creating PostgreSQL source and S3 sink connectors..."

CONNECT_POD="kafka-connect-proper-0"

# Create PostgreSQL source connector
echo "📡 Creating PostgreSQL source connector..."
kubectl exec -it $CONNECT_POD -- \
  curl -X POST -H "Content-Type: application/json" \
  --data '{
    "name": "postgres-source-connector",
    "config": {
      "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
      "database.hostname": "postgres-service",
      "database.port": "5432",
      "database.user": "postgres",
      "database.password": "postgres",
      "database.dbname": "testdb",
      "database.server.name": "postgres-server",
      "table.include.list": "public.users,public.orders",
      "plugin.name": "pgoutput",
      "slot.name": "debezium_slot",
      "publication.name": "debezium_publication",
      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable": "false",
      "value.converter.schemas.enable": "false"
    }
  }' \
  http://0.0.0.0:8083/connectors

echo ""
echo "📦 Creating S3 sink connector..."
kubectl exec -it $CONNECT_POD -- \
  curl -X POST -H "Content-Type: application/json" \
  --data '{
    "name": "s3-sink-connector",
    "config": {
      "connector.class": "io.confluent.connect.s3.S3SinkConnector",
      "tasks.max": "1",
      "topics": "postgres-server.public.users,postgres-server.public.orders",
      "s3.bucket.name": "kafka-data-lake-248189947068",
      "s3.region": "us-east-1",
      "flush.size": "3",
      "storage.class": "io.confluent.connect.s3.storage.S3Storage",
      "format.class": "io.confluent.connect.s3.format.json.JsonFormat",
      "partitioner.class": "io.confluent.connect.storage.partitioner.DefaultPartitioner",
      "key.converter": "org.apache.kafka.connect.json.JsonConverter",
      "value.converter": "org.apache.kafka.connect.json.JsonConverter",
      "key.converter.schemas.enable": "false",
      "value.converter.schemas.enable": "false"
    }
  }' \
  http://0.0.0.0:8083/connectors

echo ""
echo "✅ Connectors created! Check status:"
kubectl exec -it $CONNECT_POD -- curl http://0.0.0.0:8083/connectors
