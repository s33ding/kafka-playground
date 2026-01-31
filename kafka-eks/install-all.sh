#!/bin/bash
set -e

echo "🚀 Installing Kafka EKS Playground..."

# Deploy infrastructure
echo "📦 Deploying Kafka infrastructure..."
kubectl apply -f infrastructure/kraft-controller.yaml
kubectl apply -f infrastructure/kafka-brokers.yaml

# Wait for Kafka to be ready
echo "⏳ Waiting for Kafka to be ready..."
kubectl wait --for=condition=ready pod -l platform.confluent.io/type=kafka --timeout=300s

# Deploy PostgreSQL
echo "🐘 Deploying PostgreSQL..."
kubectl apply -f applications/postgres.yaml
kubectl wait --for=condition=ready pod -l app=postgres --timeout=180s

# Setup IAM and S3 permissions
echo "🔐 Setting up S3 permissions..."
cd iac && ./setup-s3-permissions.sh || echo "⚠️ S3 permissions already configured" && cd ..

# Deploy Kafka Connect
echo "🔌 Deploying Kafka Connect..."
cd connectors/proper-kafka-connect
./build-and-push.sh
./deploy.sh
cd ../..

# Wait for Kafka Connect
kubectl wait --for=condition=ready pod -l app=kafka-connect --timeout=300s

# Create connectors
echo "🔗 Creating connectors..."
sleep 30
kubectl exec -it $(kubectl get pods -l app=kafka-connect -o jsonpath='{.items[0].metadata.name}') -- \
  curl -X POST -H "Content-Type: application/json" \
  --data @/opt/kafka/config/postgres-source.json \
  http://localhost:8083/connectors

kubectl exec -it $(kubectl get pods -l app=kafka-connect -o jsonpath='{.items[0].metadata.name}') -- \
  curl -X POST -H "Content-Type: application/json" \
  --data @/opt/kafka/config/s3-sink-connector.json \
  http://localhost:8083/connectors

# Deploy playground app
echo "🎮 Deploying playground app..."
cd applications/kafka-playground-app
./build-push.sh
./deploy.sh
cd ../..

# Deploy monitoring
echo "📊 Deploying Kafka UI..."
kubectl apply -f applications/monitoring/kafka-ui/

echo "✅ Installation complete!"
echo "🌐 Access Kafka UI: http://app.dataiesb.com/kafka-ui"
echo "🎮 Access Playground: http://app.dataiesb.com/playground"
