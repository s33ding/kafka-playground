# Kafka on EKS - Production Data Streaming Platform

Enterprise-grade Apache Kafka deployment on Amazon EKS with CDC, S3 integration, and monitoring.

## 🏗️ Architecture

```
Applications → Kafka Cluster → S3 Storage
     ↓            (3 Brokers)       ↑
PostgreSQL → Kafka Connect ────────┘
SQL Server   (Debezium CDC)
```

## 🚀 Features

- **High Availability**: 3-broker Kafka cluster with KRaft mode
- **Change Data Capture**: Debezium connectors for PostgreSQL/SQL Server  
- **Cloud Storage**: S3 sink connector for data archival
- **Monitoring**: Kafka UI with authentication
- **Security**: IAM roles, IRSA, node isolation

## 📁 Structure

```
kafka-eks/
├── infrastructure/     # Kafka cluster & KRaft controller
├── connectors/        # Kafka Connect & S3 sink
├── applications/      # Sample apps & monitoring
├── iac/              # IAM policies & roles
└── scripts/          # Deployment automation
```

## 🚀 Quick Deploy

```bash
# Install everything
./install-all.sh

# Uninstall everything  
./uninstall-all.sh

# Access Kafka UI
open http://app.dataiesb.com/kafka-ui
```

## 🛠️ Tech Stack

- **Platform**: Amazon EKS, Kubernetes
- **Streaming**: Apache Kafka 7.4.0 (Confluent)
- **CDC**: Debezium 2.4.0
- **Storage**: Amazon S3
- **Monitoring**: Kafka UI, Prometheus

## 📊 Skills Demonstrated

- Container orchestration with Kubernetes
- Event streaming architecture
- Change Data Capture patterns
- AWS cloud integration (EKS, S3, IAM)
- Infrastructure as Code
- DevOps automation
