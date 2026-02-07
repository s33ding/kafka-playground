#!/usr/bin/env python3
import boto3
import time

athena = boto3.client('athena', region_name='us-east-1')
OUTPUT = 's3://s33ding-kafka-output/athena-results/'
DATABASE = 'bronze'

def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT}
    )
    query_id = response['QueryExecutionId']
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_id)
        status = result['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            if status != 'SUCCEEDED':
                print(f"❌ {result['QueryExecution']['Status'].get('StateChangeReason', '')}")
            return status == 'SUCCEEDED'
        time.sleep(1)

tables = [
    ('mcdonalds_sales', 'postgres-server.kafka.mcdonalds_sales'),
    ('mcdonalds_inventory', 'postgres-server.kafka.mcdonalds_inventory'),
    ('mcdonalds_employees', 'postgres-server.kafka.mcdonalds_employees')
]

for table, source_folder in tables:
    print(f"\n📦 Creating {table}...")
    temp = f"{table}_raw"
    
    run_query(f"DROP TABLE IF EXISTS {temp}")
    run_query(f"""CREATE EXTERNAL TABLE {temp} (payload string)
STORED AS TEXTFILE LOCATION 's3://s33ding-kafka-output/db_bronze/{source_folder}/'""")
    
    if run_query(f"""CREATE TABLE {table}
WITH (table_type='ICEBERG', location='s3://s33ding-kafka-output/iceberg/{table}/', is_external=false)
AS SELECT * FROM {temp}"""):
        print(f"✅ {table} created")
    
    run_query(f"DROP TABLE {temp}")

print("\n🎉 All tables created!")
