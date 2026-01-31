#!/bin/bash
set -e

echo "🔗 Creating PostgreSQL source connector..."

CONNECT_POD=$(kubectl get pods -l app=kafka-connect -o jsonpath='{.items[0].metadata.name}')

if [ -z "$CONNECT_POD" ]; then
    echo "❌ Kafka Connect pod not found"
    exit 1
fi

echo "📡 Posting connector configuration..."
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
  http://localhost:8083/connectors

echo "✅ PostgreSQL source connector created!"
