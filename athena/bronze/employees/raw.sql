CREATE EXTERNAL TABLE mcdonalds_employees_raw (
  payload string
)
STORED AS TEXTFILE
LOCATION 's3://s33ding-kafka-output/topics/postgres-server.kafka.mcdonalds_employees/';
