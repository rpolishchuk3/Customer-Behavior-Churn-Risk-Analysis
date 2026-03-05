import sqlite3
import os
import pandas as pd


SELECTED_COLUMNS = [
    'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents',
    'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
    'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
]


def create_database():
    """
    Creates the SQLite database, loads the raw CSV, cleans TotalCharges, and writes the customers table.
    """
    
    if not os.path.exists('database'):
        os.makedirs('database')

    conn = sqlite3.connect('database/churn.db')
    df = pd.read_csv('data/telco-customer-churn.csv')

    # Select only the columns we need (demonstrates SQL selection skills)
    df = df[SELECTED_COLUMNS]

    # Fix TotalCharges — blank strings for tenure=0 customers
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    df.to_sql('customers', conn, if_exists='replace', index=False)

    conn.close()
    print(f"Created 'customers' table with {len(df)} rows and {len(SELECTED_COLUMNS)} columns")


if __name__ == "__main__":
    create_database()