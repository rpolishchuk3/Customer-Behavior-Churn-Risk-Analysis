import matplotlib.pyplot as plt
import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

FIGSIZE_SM = (8, 6)
FIGSIZE_LG = (10, 6)
COLOR_NO  = '#285700'  # dark green  → No churn / Churned
COLOR_YES = '#1871BA'  # blue        → Yes churn / Active


def plot_churn_distribution(df):
    """
    Plots a bar chart showing the raw count of active vs. churned customers.
    """


    fig, ax = plt.subplots(figsize=FIGSIZE_SM)

    churn_counts = df['Churn'].value_counts().sort_index()
    bars = ax.bar(churn_counts.index, churn_counts.values, color=[COLOR_NO, COLOR_YES])

    ax.set_title("Churn Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Churn (No / Yes)", fontsize=11)
    ax.set_ylabel("Number of Customers", fontsize=11)
    ax.set_xticks(range(len(churn_counts)))
    ax.set_xticklabels(churn_counts.index, rotation=0)
    ax.grid(axis='y', alpha=0.33)
    ax.set_axisbelow(True)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height,
        f'{int(height):,}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig("outputs/churn_distribution.png", dpi=200)
    plt.close()
    print("Saved: outputs/churn_distribution.png")


def plot_churn_by_contract(df):
    """
    Plots churn rate (%) grouped by contract type as a grouped bar chart.
    """


    fig, ax = plt.subplots(figsize=FIGSIZE_LG)

    churn_rate = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100
    churn_rate.plot(kind='bar', ax=ax, color=[COLOR_NO, COLOR_YES])

    ax.set_title("Churn Rate by Contract Type", fontsize=14, fontweight='bold')
    ax.set_ylabel("Percentage (%)", fontsize=11)
    ax.set_xlabel("Contract Type", fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(axis='y', alpha=0.33)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("outputs/churn_by_contract.png", dpi=200)
    plt.close()
    print("Saved: outputs/churn_by_contract.png")


def plot_churn_by_internet(df):
    """
    Plots churn rate (%) grouped by internet service type as a grouped bar chart.
    """


    fig, ax = plt.subplots(figsize=FIGSIZE_LG)

    churn_rate = pd.crosstab(df['InternetService'], df['Churn'], normalize='index') * 100
    churn_rate.plot(kind='bar', ax=ax, color=[COLOR_NO, COLOR_YES])

    ax.set_title("Churn Rate by Internet Service", fontsize=14, fontweight='bold')
    ax.set_ylabel("Percentage (%)", fontsize=11)
    ax.set_xlabel("Internet Service", fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.grid(axis='y', alpha=0.33)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("outputs/churn_by_internet.png", dpi=200)
    plt.close()
    print("Saved: outputs/churn_by_internet.png")


def plot_monthly_charges_vs_churn(df):
    """
    Plots the average monthly charge for active vs. churned customers as a bar chart.
    """


    fig, ax = plt.subplots(figsize=FIGSIZE_SM)

    avg_charges = df.groupby('Churn')['MonthlyCharges'].mean()
    bars = ax.bar(avg_charges.index, avg_charges.values, color=[COLOR_NO, COLOR_YES])

    ax.set_title("Average Monthly Charges by Churn", fontsize=14, fontweight='bold')
    ax.set_xlabel("Churn (No / Yes)", fontsize=11)
    ax.set_ylabel("Average Monthly Charges ($)", fontsize=11)
    ax.set_xticks(range(len(avg_charges)))
    ax.set_xticklabels(avg_charges.index, rotation=0)
    ax.grid(axis='y', alpha=0.33)
    ax.set_axisbelow(True)

    for bar, value in zip(bars, avg_charges.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
        f'${value:.2f}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig("outputs/monthly_charges_vs_churn.png", dpi=200)
    plt.close()
    print("Saved: outputs/monthly_charges_vs_churn.png")


def plot_probability_distribution(risk_df):
    """
    Plots overlapping histograms of predicted churn probabilities for active and churned customers.
    """

    
    fig, ax = plt.subplots(figsize=FIGSIZE_LG)

    active_scores  = risk_df.loc[risk_df['Churn'] == 0, 'churn_risk_score']
    churned_scores = risk_df.loc[risk_df['Churn'] == 1, 'churn_risk_score']

    ax.hist(active_scores,  bins=25, alpha=0.7, color=COLOR_NO,  label='Active')
    ax.hist(churned_scores, bins=25, alpha=0.7, color=COLOR_YES, label='Churned')

    ax.set_title("Predicted Churn Probability Distribution", fontsize=14, fontweight='bold')
    ax.set_xlabel("Predicted Probability", fontsize=11)
    ax.set_ylabel("Number of Customers", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.33)
    ax.grid(axis='x', alpha=0.33)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig("outputs/probability_distribution.png", dpi=200)
    plt.close()
    print("Saved: outputs/probability_distribution.png")