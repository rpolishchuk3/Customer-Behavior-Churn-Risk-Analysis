import sqlite3
import pandas as pd

def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """

    
    conn = sqlite3.connect('database/churn.db')
    return conn

def calculate_overall_churn_rate():
    """
    Calculates the overall churn rate.
    Returns a DataFrame with total customers, churned customers, and churn rate.
    """


    conn = get_connection()
    
    query = """
        SELECT 
            COUNT(*) as total_customers,
            SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as churned_customers,
            ROUND(100.0 * SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as churn_rate_percent
        FROM customers
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def calculate_churn_by_region():
    """
    Calculates churn rate by region.
    Returns a DataFrame with churn statistics for each region.
    """


    conn = get_connection()
    
    query = """
        SELECT 
            region,
            COUNT(*) as total_customers,
            SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as churned_customers,
            ROUND(100.0 * SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as churn_rate_percent
        FROM customers
        GROUP BY region
        ORDER BY churn_rate_percent DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def calculate_spending_by_churn():
    """
    Calculates average spending by churn status.
    Returns a DataFrame with spending statistics.
    """


    conn = get_connection()
    
    query = """
        SELECT 
            c.is_active,
            COUNT(DISTINCT c.customer_id) as num_customers,
            COUNT(t.transaction_id) as total_transactions,
            ROUND(SUM(t.transaction_amount), 2) as total_spending,
            ROUND(AVG(t.transaction_amount), 2) as avg_transaction_amount
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.is_active
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

def calculate_transactions_per_customer():
    """
    Calculates average number of transactions per customer.
    Returns a DataFrame with transaction counts.
    """


    conn = get_connection()
    
    query = """
        SELECT 
            c.customer_id,
            c.is_active,
            COUNT(t.transaction_id) as transaction_count
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id, c.is_active
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df

if __name__ == "__main__":
    print("Overall Churn Rate:")
    print(calculate_overall_churn_rate())
    print("\nChurn by Region:")
    print(calculate_churn_by_region())
    print("\nSpending by Churn Status:")
    print(calculate_spending_by_churn())
    print("\nTransactions per Customer (sample):")
    print(calculate_transactions_per_customer().head())