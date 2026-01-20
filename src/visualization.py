import matplotlib.pyplot as plt
import pandas as pd
import os

from data_loader import load_customers, load_transactions
from create_features import create_customer_features
from churn_model import calculate_churn_risk
from sql_analysis import calculate_churn_by_region

def create_output_folder():
    """
    Creates the outputs folder if it doesn't exist.
    """


    if not os.path.exists('outputs'):
        os.makedirs('outputs')
        print("Created outputs folder")

def plot_spending_vs_churn(features_df):
    """
    Creates a bar chart showing average spending by churn status.
    """


    create_output_folder()
    
    spending_summary = features_df.groupby('is_active')['total_spending'].mean() # calculate average spending by churn status
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Churned', 'Active'], [spending_summary[0], spending_summary[1]], color=['#285700', '#1871BA'])
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'${height:.2f}', ha='center', va='bottom', fontsize=11)
    
    plt.title('Average Total Spending by Churn Status', fontsize=14, fontweight='bold')
    plt.ylabel('Average Total Spending ($)', fontsize=11)
    plt.xlabel('Customer Status', fontsize=11)
    plt.grid(axis='y', alpha=0.333)
    

    plt.tight_layout()
    plt.savefig('outputs/spending_vs_churn.png', dpi=200)
    plt.close()
    
    print("Saved: outputs/spending_vs_churn.png")

def plot_transactions_vs_churn(features_df):
    """
    Creates a bar chart showing average transaction count by churn status.
    """


    create_output_folder()

    transaction_summary = features_df.groupby('is_active')['transaction_count'].mean()
    
    plt.figure(figsize=(8, 6))
    bars = plt.bar(['Churned', 'Active'], [transaction_summary[0], transaction_summary[1]], color=['#285700', '#1871BA'])
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}',ha='center', va='bottom', fontsize=11)
    
    plt.title('Average Transaction Count by Churn Status', fontsize=14, fontweight='bold')
    plt.ylabel('Average Number of Transactions', fontsize=11)
    plt.xlabel('Customer Status', fontsize=11)
    plt.grid(axis='y', alpha=0.333)
    
    plt.tight_layout()
    plt.savefig('outputs/transactions_vs_churn.png', dpi=200)
    plt.close()
    
    print("Saved: outputs/transactions_vs_churn.png")

def plot_churn_by_region(churn_by_region_df):
    """
    Creates a bar chart showing churn rate by region.
    """


    create_output_folder()
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(churn_by_region_df['region'], churn_by_region_df['churn_rate_percent'], color='#285700')
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}%', ha='center', va='bottom', fontsize=11)
    
    plt.title('Churn Rate by Region', fontsize=14, fontweight='bold')
    plt.ylabel('Churn Rate (%)', fontsize=11)
    plt.xlabel('Region', fontsize=11)
    plt.grid(axis='y', alpha=0.333)
    plt.ylim(0, max(churn_by_region_df['churn_rate_percent']) * 1.2)
    
    plt.tight_layout()
    plt.savefig('outputs/churn_by_region.png', dpi=200)
    plt.close()
    
    print("Saved: outputs/churn_by_region.png")

def plot_risk_distribution(risk_scores_df):
    """
    Creates a histogram showing the distribution of churn risk scores.
    """


    create_output_folder()
    
    active_risks = risk_scores_df[risk_scores_df['is_active'] == 1]['churn_risk_score']
    churned_risks = risk_scores_df[risk_scores_df['is_active'] == 0]['churn_risk_score']

    plt.figure(figsize=(10, 6))
    plt.hist([active_risks, churned_risks], bins=10, label=['Active', 'Churned'], color=['#1871BA', '#285700'])
    
    plt.title('Distribution of Churn Risk Scores', fontsize=14, fontweight='bold')
    plt.xlabel('Churn Risk Score', fontsize=11)
    plt.ylabel('Number of Customers', fontsize=11)
    plt.legend(fontsize=11)
    plt.grid(axis='y', alpha=0.333)
    
    plt.tight_layout()
    plt.savefig('outputs/risk_distribution.png', dpi=200)
    plt.close()
    
    print("Saved: outputs/risk_distribution.png")

if __name__ == "__main__":
    customers = load_customers()
    transactions = load_transactions()
    features = create_customer_features(customers, transactions)
    risk_scores = calculate_churn_risk(features)
    churn_by_region = calculate_churn_by_region()
    
    print("\nCreating visualizations...")
    plot_spending_vs_churn(features)
    plot_transactions_vs_churn(features)
    plot_churn_by_region(churn_by_region)
    plot_risk_distribution(risk_scores)
    print("\nAll visualizations created successfully!")