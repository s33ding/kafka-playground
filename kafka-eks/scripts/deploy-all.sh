#!/bin/bash
set -e

echo "🚀 Deploying Kafka on EKS..."

# Deploy infrastructure
echo "📦 Deploying Kafka infrastructure..."
kubectl apply -f infrastructure/

# Wait for Kafka to be ready
echo "⏳ Waiting for Kafka cluster to be ready..."
kubectl wait --for=condition=Ready kafka/kafka-brokers --timeout=300s

# Deploy Kafka Connect
echo "🔌 Deploying Kafka Connect..."
kubectl apply -f connectors/proper-kafka-connect/

# Wait for Connect to be ready
echo "⏳ Waiting for Kafka Connect to be ready..."
kubectl wait --for=condition=Ready connect/kafka-connect-proper --timeout=300s

# Deploy applications
echo "📱 Deploying applications..."
kubectl apply -f applications/

echo "✅ Deployment complete!"
echo "🌐 Access Kafka UI at: http://app.dataiesb.com/kafka-ui"
