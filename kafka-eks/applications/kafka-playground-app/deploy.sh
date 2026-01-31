#!/bin/bash

echo "Adding Kafka Playground App to existing ingress..."

# Add the new path to the existing ingress
kubectl patch ingress ingress-iesb --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/rules/0/http/paths/-",
    "value": {
      "backend": {
        "service": {
          "name": "kafka-playground-service",
          "port": {
            "number": 80
          }
        }
      },
      "path": "/kafka-src-app",
      "pathType": "Prefix"
    }
  }
]'

echo "Kafka Playground App added to ingress!"
echo "Access via: https://app.dataiesb.com/kafka-src-app"
