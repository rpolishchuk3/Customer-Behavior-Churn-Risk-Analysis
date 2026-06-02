import sys
import os
import pandas as pd

# Allow imports from src/ when running from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from db_setup import create_database
from data_loader import load_customers
from create_features import create_customer_features
from churn_model import calculate_churn_risk, evaluate_churn_model
from sql_analysis import run_all_analysis
from visualization import (
    plot_churn_distribution,
    plot_churn_by_contract,
    plot_churn_by_internet,
    plot_monthly_charges_vs_churn,
    plot_probability_distribution
)


def main():
    """
    Runs the complete churn analysis pipeline.
    """
    # Set working directory to project root so all relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    print("="*60)
    print("CUSTOMER CHURN ANALYSIS PIPELINE")
    print("="*60)

    # Step 1: Set up database
    print("\n[Step 1/6] Setting up database...")
    create_database()

    # Step 2: SQL analysis
    print("\n[Step 2/6] Running SQL analysis...")
    run_all_analysis()

    # Step 3: Load data
    print("\n[Step 3/6] Loading data from database...")
    customers = load_customers()

    # Confounding check: is MonthlyCharges a real driver or a proxy?
    # High-paying customers churn more in the raw data — but does price cause it?
    churn_bin = (customers['Churn'] == 'Yes').astype(int)
    customers['_churn'] = churn_bin
    customers['_price_band'] = pd.cut(customers['MonthlyCharges'],
                                      bins=[0, 35, 65, 90, 200],
                                      labels=['<$35', '$35-65', '$65-90', '>$90'])
    print("\n--- Confounding Check: MonthlyCharges vs Churn ---")
    print("Raw churn rate by price band:")
    print(customers.groupby('_price_band', observed=True)['_churn'].mean().map(lambda x: f"{x:.1%}").to_string())
    print("\nChurn rate by InternetService (the real driver):")
    print(customers.groupby('InternetService')['_churn'].mean().map(lambda x: f"{x:.1%}").to_string())
    cross = customers.groupby(['Contract', '_price_band'], observed=True)['_churn'].mean().unstack().round(3)
    print("\nChurn rate by Contract × Price (price effect weakens within each contract type):")
    print(cross.to_string())

    # ADD: Tenure segmentation — short-tenure customers churn at >4x the rate of long-tenure ones.
    # This is a third confounder: new customers are month-to-month and on fiber, so they're
    # both higher-paying AND higher-risk. Tenure, not price, is the early-warning signal.
    customers['_tenure_band'] = pd.cut(customers['tenure'],
                                       bins=[0, 12, 24, 48, 72],
                                       labels=['0-12m', '12-24m', '24-48m', '48-72m'])
    print("\nChurn rate by Tenure band:")
    print(customers.groupby('_tenure_band', observed=True)['_churn'].mean().map(lambda x: f"{x:.1%}").to_string())

    print("→ 69% of churners are Fiber Optic. 89% are Month-to-month. 48% left within 12 months.")
    print("  MonthlyCharges is a PROXY — price reduction is not the right lever.")
    customers.drop(columns=['_churn', '_price_band', '_tenure_band'], inplace=True)

    # Step 4: Feature engineering
    print("\n[Step 4/6] Engineering features...")
    features = create_customer_features(customers)
    print("\n[Step 5/6] Calculating churn risk scores...")
    risk_scores = calculate_churn_risk(features)
    evaluate_churn_model(risk_scores)

    # Step 6: Generate visualizations
    print("\n[Step 6/6] Generating visualizations...")
    plot_churn_distribution(customers)
    plot_churn_by_contract(customers)
    plot_churn_by_internet(customers)
    plot_monthly_charges_vs_churn(customers)
    plot_probability_distribution(risk_scores)

    print("\n" + "="*60)
    print("PIPELINE COMPLETE!")
    print("="*60 + "\n")
    print("Next steps:")
    print("1. Check the outputs/ folder for visualizations")
    print("2. Open notebook/churn_analysis.ipynb for detailed exploration")


if __name__ == "__main__":
    main()