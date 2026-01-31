# Kafka Connectors

Kafka Connect deployment with custom image containing Debezium and S3 connectors.

## Components

- **proper-kafka-connect/**: Main Kafka Connect cluster
- **s3-sink/**: S3 sink connector configuration

## Custom Image

Built with:
- Debezium PostgreSQL Connector 2.4.0
- Confluent S3 Sink Connector 10.5.0

## Deploy

```bash
kubectl apply -f connectors/proper-kafka-connect/
```
