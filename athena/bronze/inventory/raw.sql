CREATE EXTERNAL TABLE mcdonalds_inventory_raw (
  payload string
)
STORED AS TEXTFILE
LOCATION 's3://s33ding-kafka-output/topics/postgres-server.kafka.mcdonalds_inventory/';
