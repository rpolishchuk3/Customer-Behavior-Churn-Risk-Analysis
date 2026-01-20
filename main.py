import sys
import os

from db_setup import create_database
from data_loader import load_customers, load_transactions
from sql_analysis import (calculate_overall_churn_rate, 
                          calculate_churn_by_region,
                          calculate_spending_by_churn)
from create_features import create_customer_features
from churn_model import calculate_churn_risk, evaluate_churn_model
from visualization import (plot_spending_vs_churn,
                           plot_transactions_vs_churn,
                           plot_churn_by_region,
                           plot_risk_distribution)


sys.path.append('src')

def main():
    """
    Runs the complete churn analysis pipeline.
    """
    

    print("="*60)
    print("CUSTOMER CHURN ANALYSIS PIPELINE")
    print("="*60)
    
    # Step 1: Set up database
    print("\n[Step 1/6] Setting up database...")
    create_database()
    
    # Step 2: Load data
    print("\n[Step 2/6] Loading data from database...")
    customers = load_customers()
    transactions = load_transactions()
    
    # Step 3: Run SQL analysis
    print("\n[Step 3/6] Running SQL analysis...")
    
    overall_churn = calculate_overall_churn_rate()
    print("\n----- Overall Churn Rate -----")
    print(overall_churn.to_string(index=False))
    
    churn_by_region = calculate_churn_by_region()
    print("\n----- Churn Rate by Region -----")
    print(churn_by_region.to_string(index=False))
    
    spending_by_churn = calculate_spending_by_churn()
    print("\n----- Spending by Churn Status -----")
    print(spending_by_churn.to_string(index=False))
    
    # Step 4: Create create_features
    print("\n[Step 4/6] Customer create_features...")
    create_features = create_customer_features(customers, transactions)
    
    # Step 5: Calculate churn risk
    print("\n[Step 5/6] Calculating churn risk scores...")
    risk_scores = calculate_churn_risk(create_features)
    evaluate_churn_model(risk_scores)
    
    # Step 6: Generate visualizations
    print("\n[Step 6/6] Generating visualizations...")
    plot_spending_vs_churn(create_features)
    plot_transactions_vs_churn(create_features)
    plot_churn_by_region(churn_by_region)
    plot_risk_distribution(risk_scores)
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE!")
    print("="*60 + "\n")
    print("Next steps:")
    print("1. Check the outputs/ folder for visualizations")
    print("2. Open notebook/churn_analysis.ipynb for detailed exploration")
    print("3. Review database/churn.db for SQL queries")

if __name__ == "__main__":
    main()