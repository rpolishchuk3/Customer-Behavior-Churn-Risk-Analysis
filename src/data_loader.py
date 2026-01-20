import sqlite3
import pandas as pd

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """


    conn = sqlite3.connect('database/churn.db')
    return conn

def load_customers():
    """
    Loads the customers table from the database.
    Returns a pandas DataFrame.
    """


    conn = get_connection()
    query = "SELECT * FROM customers"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    print(f"Loaded {len(df)} customers")
    return df

def load_transactions():
    """
    Loads the transactions table from the database.
    Returns a pandas DataFrame.
    """


    conn = get_connection()
    query = "SELECT * FROM transactions"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    
    print(f"Loaded {len(df)} transactions")
    return df

if __name__ == "__main__":
    customers = load_customers()
    transactions = load_transactions()
    print("\nCustomers sample:")
    print(customers.head())
    print("\nTransactions sample:")
    print(transactions.head())