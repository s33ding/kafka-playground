#!/bin/bash

# Create topic
kubectl exec -n lab kafka-brokers-0 -- kafka-topics \
    --create \
    --bootstrap-server kafka-brokers:9092 \
    --topic postgres.public.users \
    --partitions 3 \
    --replication-factor 3
