#!/bin/bash
set -e

echo "🚀 Installing Kafka on EKS - Complete Setup"

# Add Confluent Helm repository
echo "📦 Adding Confluent Helm repository..."
helm repo add confluentinc https://packages.confluent.io/helm
helm repo update

# Install Confluent Operator
echo "⚙️ Installing Confluent Operator..."
helm upgrade --install confluent-operator confluentinc/confluent-for-kubernetes

# Wait for operator to be ready
echo "⏳ Waiting for Confluent Operator..."
kubectl wait --for=condition=available deployment/confluent-operator --timeout=300s

# Deploy KRaft Controller
echo "🎛️ Deploying KRaft Controller..."
kubectl apply -f infrastructure/kraft-controller.yaml

# Wait for KRaft Controller
echo "⏳ Waiting for KRaft Controller..."
kubectl wait --for=condition=Ready kraftcontroller/kraftcontroller --timeout=300s

# Deploy Kafka Brokers
echo "☕ Deploying Kafka Brokers..."
kubectl apply -f infrastructure/kafka-brokers.yaml

# Wait for Kafka Brokers
echo "⏳ Waiting for Kafka Brokers..."
kubectl wait --for=condition=Ready kafka/kafka-brokers --timeout=600s

# Setup IAM permissions
echo "🔐 Setting up S3 permissions..."
cd iac && ./setup-s3-permissions.sh && cd ..

# Deploy Kafka Connect
echo "🔌 Deploying Kafka Connect..."
kubectl apply -f connectors/proper-kafka-connect/kafka-connect.yaml

# Wait for Kafka Connect
echo "⏳ Waiting for Kafka Connect..."
kubectl wait --for=condition=Ready connect/kafka-connect-proper --timeout=300s

# Deploy Kafka UI
echo "🖥️ Deploying Kafka UI..."
kubectl apply -f applications/monitoring/kafka-ui/

echo "✅ Installation Complete!"
echo ""
echo "🌐 Access Points:"
echo "   Kafka UI: http://app.dataiesb.com/kafka-ui"
echo "   Kafka Connect: kubectl port-forward kafka-connect-proper-0 8083:8083"
echo ""
echo "📊 Check Status:"
echo "   kubectl get kafka,kraftcontroller,connect"
