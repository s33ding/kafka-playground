#!/bin/bash
set -e

echo "🌐 Setting up port forwards for Kafka EKS services..."

# Function to start port forward in background
start_port_forward() {
    local service=$1
    local local_port=$2
    local remote_port=$3
    
    echo "📡 Forwarding $service: localhost:$local_port -> $remote_port"
    kubectl port-forward svc/$service $local_port:$remote_port &
    echo $! > /tmp/pf-$service.pid
}

# Kill existing port forwards
pkill -f "kubectl port-forward" 2>/dev/null || true
rm -f /tmp/pf-*.pid 2>/dev/null || true

# Start port forwards
start_port_forward "kafka-ui" 8080 80
start_port_forward "kafka-playground-service" 8081 80
start_port_forward "postgres-service" 5432 5432
start_port_forward "kafka-connect-proper" 8083 8083

echo ""
echo "✅ Port forwards active:"
echo "🎮 Playground App: http://localhost:8081"
echo "📊 Kafka UI: http://localhost:8080"
echo "🐘 PostgreSQL: localhost:5432"
echo "🔌 Kafka Connect: http://localhost:8083"
echo ""
echo "Press Ctrl+C to stop all port forwards"

# Wait for interrupt
trap 'echo "🛑 Stopping port forwards..."; pkill -f "kubectl port-forward"; rm -f /tmp/pf-*.pid; exit 0' INT
wait
