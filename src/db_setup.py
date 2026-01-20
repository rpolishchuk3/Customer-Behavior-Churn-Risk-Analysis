import sqlite3
import os

def create_database():
    """
    Creates the SQLite database and tables for customers and transactions.
    Inserts data from CSV files into the tables.
    """
    

    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect('database/churn.db')
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS transactions')
    cursor.execute('DROP TABLE IF EXISTS customers')
    
    cursor.execute('''
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            signup_date TEXT,
            region TEXT,
            plan_type TEXT,
            is_active INTEGER
        )
    ''')
    print("Created customers table")
    
    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            transaction_date TEXT,
            transaction_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')
    print("Created transactions table")
    
    with open('data/customers.csv', 'r') as file:
        next(file)
        for line in file:
            values = line.strip().split(',')
            cursor.execute('''INSERT INTO customers VALUES (?, ?, ?, ?, ?)''', values)
    
    print("Inserted customer data")
    
    with open('data/transactions.csv', 'r') as file:
        next(file)
        for line in file:
            values = line.strip().split(',')
            cursor.execute('''
                INSERT INTO transactions VALUES (?, ?, ?, ?)
            ''', values)
    
    print("Inserted transaction data")
    
    conn.commit()
    conn.close()
    
    print("\nDatabase setup complete!")
    print("Database location: database/churn.db")

if __name__ == "__main__":
    create_database()