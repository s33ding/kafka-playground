import boto3
import time

client = boto3.client('athena', region_name='us-east-1')

def register_iceberg_table(table_name, s3_location):
    query = f"""
    CREATE TABLE IF NOT EXISTS bronze.{table_name}
    LOCATION '{s3_location}'
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
            print(f"✅ {table_name}: {status}")
            if status == 'FAILED':
                print(f"   Error: {result['QueryExecution']['Status'].get('StateChangeReason', '')}")
            break
        time.sleep(1)

if __name__ == '__main__':
    tables = [
        ('mcdonalds_sales_kafka', 's3://s33ding-kafka-output/topics/postgres-server.kafka.mcdonalds_sales/'),
        ('mcdonalds_inventory_kafka', 's3://s33ding-kafka-output/topics/postgres-server.kafka.mcdonalds_inventory/'),
        ('mcdonalds_employees_kafka', 's3://s33ding-kafka-output/topics/postgres-server.kafka.mcdonalds_employees/')
    ]
    
    for table_name, location in tables:
        register_iceberg_table(table_name, location)
