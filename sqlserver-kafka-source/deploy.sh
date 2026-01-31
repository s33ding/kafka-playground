#!/bin/bash

echo "Deploying SQL Server..."
kubectl apply -f sqlserver-init.yaml
kubectl apply -f sqlserver-deployment.yaml

echo "Waiting for SQL Server to be ready..."
kubectl wait --for=condition=ready pod -l app=sqlserver --timeout=300s

echo "SQL Server deployed successfully!"
echo "Connection details:"
echo "  Host: sqlserver-service"
echo "  Port: 1433"
echo "  Database: TestDB"
echo "  Username: sa"
echo "  Password: YourStrong@Passw0rd"
