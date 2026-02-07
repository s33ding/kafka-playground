import boto3
import time

client = boto3.client('athena', region_name='us-east-1')

query = """
CREATE TABLE bronze.mcdonalds_sales_bronze (
  payload string
)
LOCATION 's3://s33ding-kafka-output/db_bronze/mcdonalds_sales/'
TBLPROPERTIES ('table_type'='ICEBERG')
"""

response = client.start_query_execution(
    QueryString=query,
    ResultConfiguration={'OutputLocation': 's3://s33ding-kafka-output/athena-results/'},
    WorkGroup='primary'
)

query_id = response['QueryExecutionId']

while True:
    result = client.get_query_execution(QueryExecutionId=query_id)
    status = result['QueryExecution']['Status']['State']
    if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        print(f"Status: {status}")
        if status == 'FAILED':
            print(f"Error: {result['QueryExecution']['Status'].get('StateChangeReason', '')}")
        break
    time.sleep(1)
