import boto3
import time

client = boto3.client('athena', region_name='us-east-1')

def run_insert(query, description):
    print(f"\n📥 {description}")
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
            if status == 'SUCCEEDED':
                print(f"✅ {description} completed")
            else:
                print(f"❌ Failed: {result['QueryExecution']['Status'].get('StateChangeReason', '')}")
            break
        time.sleep(1)

if __name__ == '__main__':
    tables = [
        ('mcdonalds_sales', 'Sales'),
        ('mcdonalds_inventory', 'Inventory'),
        ('mcdonalds_employees', 'Employees')
    ]
    
    for table, name in tables:
        query = f"INSERT INTO bronze.{table}_bronze SELECT payload FROM default.{table}_raw"
        run_insert(query, f"Loading {name} data")
