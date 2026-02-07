import boto3
import time

athena = boto3.client('athena', region_name='us-east-1')

def show_schema(table):
    query = f"SELECT * FROM bronze.{table} LIMIT 1"
    response = athena.start_query_execution(
        QueryString=query,
        ResultConfiguration={'OutputLocation': 's3://s33ding-kafka-output/athena-results/'}
    )
    
    qid = response['QueryExecutionId']
    while True:
        result = athena.get_query_execution(QueryExecutionId=qid)
        if result['QueryExecution']['Status']['State'] in ['SUCCEEDED', 'FAILED']:
            break
        time.sleep(1)
    
    if result['QueryExecution']['Status']['State'] == 'SUCCEEDED':
        results = athena.get_query_results(QueryExecutionId=qid)
        print(f"\n{'='*60}")
        print(f"📋 {table} Schema")
        print('='*60)
        for col in results['ResultSet']['Rows'][0]['Data']:
            print(f"  • {col.get('VarCharValue', 'N/A')}")

for table in ['mcdonalds_sales_raw', 'mcdonalds_inventory_raw', 'mcdonalds_employees_raw']:
    show_schema(table)
