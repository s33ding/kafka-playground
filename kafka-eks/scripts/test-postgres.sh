#!/bin/bash
set -e

echo "🧪 Testing PostgreSQL connection and data..."

POSTGRES_POD=$(kubectl get pods -l app=postgres -o jsonpath='{.items[0].metadata.name}')

echo "📊 Testing database connection..."
kubectl exec -it $POSTGRES_POD -- psql -U postgres -d testdb -c "\dt"

echo "👥 Users table:"
kubectl exec -it $POSTGRES_POD -- psql -U postgres -d testdb -c "SELECT * FROM users;"

echo "📦 Orders table:"
kubectl exec -it $POSTGRES_POD -- psql -U postgres -d testdb -c "SELECT * FROM orders;"

echo "✅ PostgreSQL test completed successfully!"
