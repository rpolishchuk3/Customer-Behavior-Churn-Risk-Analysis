import pandas as pd
import numpy as np

from data_loader import load_customers, load_transactions
from create_features import create_customer_features


def calculate_churn_risk(features_df):
    """
    Calculates a simple churn risk score based on customer behavior.
    
    Uses a rule-based approach:
    - Low transaction count increases risk
    - Low spending increases risk
    - Short term increases risk
    
    Returns a DataFrame with customer_id and churn_risk_score.
    """
    

    df = features_df.copy() # create a copy to avoid modifying original data
    
    df['churn_risk_score'] = 0.0

    # customers with fewer transactions are more likely to churn
    # give higher risk to customers with less than 3 transactions
    df['risk_low_transactions'] = np.where(df['transaction_count'] < 3, 0.4, 0.1)
    
    # customers who spend less are more likely to churn
    # calculate median spending
    median_spending = df['total_spending'].median()
    df['risk_low_spending'] = np.where(df['total_spending'] < median_spending, 0.3, 0.1)
    
    # newer customers might be more likely to churn
    # give higher risk to customers with less than 100 days term
    df['risk_short_term'] = np.where(df['term_days'] < 100, 0.2, 0.05)
    
    # calculate total risk score (sum of risk factors)
    df['churn_risk_score'] = (
        df['risk_low_transactions'] + 
        df['risk_low_spending'] + 
        df['risk_short_term']
    )
    
    # Normalize to 0-1 range
    df['churn_risk_score'] = df['churn_risk_score'].clip(upper=1.0)
    df['churn_risk_score'] = df['churn_risk_score'].round(3)
    

    result = df[['customer_id', 'is_active', 'churn_risk_score']]
    
    print(f"Calculated churn risk for {len(result)} customers")
    
    return result

def evaluate_churn_model(risk_scores_df):
    """
    Evaluates the churn risk model by comparing scores for active vs churned customers.
    """
    

    active = risk_scores_df[risk_scores_df['is_active'] == 1]
    churned = risk_scores_df[risk_scores_df['is_active'] == 0]
    
    avg_risk_active = active['churn_risk_score'].mean()
    avg_risk_churned = churned['churn_risk_score'].mean()
    
    print("\n=== Churn Risk Model Evaluation ===")
    print(f"Average risk score for active customers: {avg_risk_active:.2f}")
    print(f"Average risk score for churned customers: {avg_risk_churned:.2f}")
    print(f"Difference: {abs(avg_risk_churned - avg_risk_active):.2f}")
    
    print(f"\nActive customers: {len(active)}")
    print(f"Churned customers: {len(churned)}")

if __name__ == "__main__":
    customers = load_customers()
    transactions = load_transactions()
    features = create_customer_features(customers, transactions)
    
    risk_scores = calculate_churn_risk(features)
    print("\nSample risk scores:")
    print(risk_scores.head(10))
    
    evaluate_churn_model(risk_scores)