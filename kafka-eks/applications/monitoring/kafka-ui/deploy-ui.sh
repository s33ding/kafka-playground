#!/bin/bash

echo "Deploying Kafka UI..."
kubectl apply -f kafka-ui.yaml

echo "Waiting for Kafka UI to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/kafka-ui

echo "Kafka UI deployed successfully!"
echo "Access via: kubectl port-forward svc/kafka-ui 8080:8080"
echo "Then open: http://localhost:8080"
