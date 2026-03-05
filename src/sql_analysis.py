import sqlite3
import pandas as pd


def get_connection():
    return sqlite3.connect('database/churn.db')


def overall_churn_rate(conn):
    query = (
        "SELECT"
        " COUNT(*) AS total_customers,"
        " SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,"
        " ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct"
        " FROM customers"
    )
    return pd.read_sql_query(query, conn)


def churn_rate_by_contract(conn):
    query = (
        "SELECT"
        " Contract,"
        " COUNT(*) AS total_customers,"
        " SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,"
        " ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct"
        " FROM customers"
        " GROUP BY Contract"
        " ORDER BY churn_rate_pct DESC"
    )
    return pd.read_sql_query(query, conn)


def churn_rate_by_internet_service(conn):
    query = (
        "SELECT"
        " InternetService,"
        " COUNT(*) AS total_customers,"
        " SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,"
        " ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct"
        " FROM customers"
        " GROUP BY InternetService"
        " ORDER BY churn_rate_pct DESC"
    )
    return pd.read_sql_query(query, conn)


def avg_monthly_charges_by_churn(conn):
    query = (
        "SELECT"
        " Churn,"
        " ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,"
        " ROUND(AVG(TotalCharges), 2) AS avg_total_charges,"
        " COUNT(*) AS customer_count"
        " FROM customers"
        " GROUP BY Churn"
    )
    return pd.read_sql_query(query, conn)


def run_all_analysis():
    conn = get_connection()

    print("\n--- Overall Churn Rate ---")
    print(overall_churn_rate(conn).to_string(index=False))

    print("\n--- Churn Rate by Contract Type ---")
    print(churn_rate_by_contract(conn).to_string(index=False))

    print("\n--- Churn Rate by Internet Service ---")
    print(churn_rate_by_internet_service(conn).to_string(index=False))

    print("\n--- Average Charges by Churn Status ---")
    print(avg_monthly_charges_by_churn(conn).to_string(index=False))

    conn.close()


if __name__ == "__main__":
    run_all_analysis()