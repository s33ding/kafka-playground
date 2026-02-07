#!/usr/bin/env python3
import subprocess
import random
import uuid

def get_pod():
    result = subprocess.run(
        "kubectl get pods -n lab -l app=postgres -o jsonpath='{.items[0].metadata.name}'",
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip()

def random_insert(count=10):
    products = [
        {"code": "BIG001", "name": "Big Mac", "category": "Burgers", "price": 15.90},
        {"code": "QUA001", "name": "Quarterão", "category": "Burgers", "price": 18.90},
        {"code": "CHE001", "name": "Cheeseburger", "category": "Burgers", "price": 9.90},
        {"code": "NUG001", "name": "McNuggets 10un", "category": "Chicken", "price": 16.90},
        {"code": "FRY001", "name": "Batata Frita M", "category": "Sides", "price": 8.50},
        {"code": "COK001", "name": "Coca-Cola 500ml", "category": "Beverages", "price": 6.90}
    ]
    
    payment_methods = ["credit_card", "debit_card", "pix", "cash"]
    regions = ["Southeast", "Northeast", "South"]
    cities = ["São Paulo", "Rio de Janeiro", "Recife", "Curitiba"]
    positions = ["Cashier", "Cook", "Manager", "Cleaner"]
    shifts = ["morning", "afternoon", "night"]
    
    pod = get_pod()
    
    for i in range(count):
        store_id = random.randint(1, 100)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        txn_id = str(uuid.uuid4())[:8]
        
        # Insert sales
        sql = f"""INSERT INTO kafka.mcdonalds_sales 
            (store_id, store_name, transaction_id, product_code, product_name, 
             category, quantity, unit_price, total_amount, payment_method, region, city) 
            VALUES ({store_id}, 'McDonalds Store {store_id}', 'TXN_{txn_id}', 
                    '{product["code"]}', '{product["name"]}', '{product["category"]}', 
                    {quantity}, {product["price"]}, {round(quantity * product["price"], 2)}, 
                    '{random.choice(payment_methods)}', '{random.choice(regions)}', '{random.choice(cities)}');"""
        subprocess.run(f'kubectl exec -n lab {pod} -- psql -U postgres -d testdb -c "{sql}"', 
                      shell=True, capture_output=True)
        
        # Insert inventory
        stock = random.randint(20, 150)
        sql = f"""INSERT INTO kafka.mcdonalds_inventory 
            (store_id, product_code, product_name, current_stock, min_stock, max_stock) 
            VALUES ({store_id}, '{product["code"]}', '{product["name"]}', 
                    {stock}, 20, 200);"""
        subprocess.run(f'kubectl exec -n lab {pod} -- psql -U postgres -d testdb -c "{sql}"', 
                      shell=True, capture_output=True)
        
        # Insert employee
        emp_id = f"EMP{random.randint(1000, 9999)}"
        sql = f"""INSERT INTO kafka.mcdonalds_employees 
            (store_id, employee_id, name, position, hire_date, shift, hourly_rate) 
            VALUES ({store_id}, '{emp_id}', 'Employee {emp_id}', 
                    '{random.choice(positions)}', '2024-01-01', 
                    '{random.choice(shifts)}', {round(random.uniform(15, 30), 2)});"""
        subprocess.run(f'kubectl exec -n lab {pod} -- psql -U postgres -d testdb -c "{sql}"', 
                      shell=True, capture_output=True)
        
        if (i + 1) % 5 == 0:
            print(f"Inserted {i + 1}/{count} records into all 3 tables")
    
    print(f"✅ Completed: {count} records inserted into sales, inventory, and employees")

if __name__ == "__main__":
    random_insert()
