#!/usr/bin/env python3
import boto3

athena = boto3.client('athena', region_name='us-east-1')
OUTPUT = 's3://s33ding-kafka-output/athena-results/'
DATABASE = 'bronze'

tables = [
    ('sales', 'mcdonalds_sales'),
    ('inventory', 'mcdonalds_inventory'),
    ('employees', 'mcdonalds_employees')
]

for folder, table in tables:
    print(f"\n📦 Creating {table}...")
    
    with open(f'{folder}/bronze.sql') as f:
        query = f.read()
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT}
    )
    print(f"✅ {table} created")

print("\n🎉 All tables created!")
