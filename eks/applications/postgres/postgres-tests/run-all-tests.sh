#!/bin/bash
set -e

echo "🧪 Running PostgreSQL Integration Tests..."

./check-connection.sh
echo ""
./check-mcdonalds.sh
echo ""
./insert-mcdonalds-data.sh
echo ""
./query-mcdonalds.sh

echo ""
echo "✅ All PostgreSQL tests completed!"
