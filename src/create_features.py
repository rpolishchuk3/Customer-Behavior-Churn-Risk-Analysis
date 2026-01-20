import pandas as pd

from datetime import datetime
from data_loader import load_customers, load_transactions

def create_customer_features(customers_df, transactions_df):
    """
    Creates customer-level features for churn analysis.
    
    Parameters:
    - customers_df: DataFrame with customer information
    - transactions_df: DataFrame with transaction information
    
    Returns:
    - DataFrame with customer features and churn label
    """

    
    # calculate transaction-based features for each customer
    transaction_features = transactions_df.groupby('customer_id').agg({
        'transaction_amount': ['sum', 'mean', 'count']
    }).reset_index()

    transaction_features.columns = ['customer_id', 'total_spending', 'avg_transaction_amount', 'transaction_count']
    
    features = customers_df.merge(transaction_features, on='customer_id', how='left') # merge with customer data
    
    # fill missing values with 0 (for customers with no transactions)
    features['total_spending'] = features['total_spending'].fillna(0)
    features['avg_transaction_amount'] = features['avg_transaction_amount'].fillna(0)
    features['transaction_count'] = features['transaction_count'].fillna(0)
    
    
    
    reference_date = datetime(2025, 8, 1)
    features['signup_date'] = pd.to_datetime(features['signup_date'])
    features['term_days'] = (reference_date - features['signup_date']).dt.days
    
    features['total_spending'] = features['total_spending'].round(2)
    features['avg_transaction_amount'] = features['avg_transaction_amount'].round(2)
    
    print(f"Created features for {len(features)} customers")
    print(f"Feature columns: {list(features.columns)}")
    
    return features

if __name__ == "__main__":
    customers = load_customers()
    transactions = load_transactions()
    
    features = create_customer_features(customers, transactions)
    print("\nSample features:")
    print(features.head())
    print("\nFeature statistics:")
    print(features[['total_spending', 'avg_transaction_amount', 'transaction_count', 'term_days']].describe())