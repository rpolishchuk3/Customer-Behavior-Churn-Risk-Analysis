import sys
import os

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

    # Step 4: Feature engineering
    print("\n[Step 4/6] Engineering features...")
    features = create_customer_features(customers)

    # Step 5: Train churn model
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