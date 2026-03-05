import sqlite3
import pandas as pd

def get_connection():
    """
    Returns a SQLite connection to the churn database.
    """

    
    conn = sqlite3.connect('database/churn.db')
    return conn

def load_customers():
    """
    Loads the full customers table from the SQLite database into a pandas DataFrame.
    """


    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM customers", conn)
    conn.close()
    print(f"Loaded {len(df)} customers")
    return df

if __name__ == "__main__":
    customers = load_customers()
    print("\nCustomers sample:")
    print(customers.head())