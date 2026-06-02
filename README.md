# Customer Behavior & Churn Risk Analysis

An end-to-end data analytics pipeline for predicting customer churn on the Telco dataset. The project covers raw data ingestion into SQLite, SQL-driven KPI analysis, feature engineering, a logistic regression risk model, and a confounding analysis that challenges the most intuitive (and incorrect) interpretation of the data.

---

## Business Problem

Customer churn is one of the most expensive problems in subscription businesses. Acquiring a new customer costs 5–7× more than retaining an existing one, and churn erodes both revenue and LTV predictability.

This project goes beyond measuring churn - it identifies **which customers are at risk, why, and what the wrong explanations are**. The final output is a scored customer list that retention teams can act on directly.

Four questions drive the analysis:

1. What is the overall churn rate, and how does it segment by contract type and service?
2. Do higher-paying customers churn more - and if so, why?
3. Which features actually predict churn in a controlled model?
4. Can we assign each customer a reliable churn probability score?

---

## Dataset

Source: [Telco Customer Churn - Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)

7,043 customers | 21 features | 26.5% churn rate

| Field | Description |
|-------|-------------|
| `customerID` | Unique identifier (dropped before modelling) |
| `gender`, `SeniorCitizen`, `Partner`, `Dependents` | Demographics |
| `tenure` | Months with the company |
| `PhoneService`, `MultipleLines`, `InternetService` | Service type |
| `OnlineSecurity`, `TechSupport`, `StreamingTV`, etc. | Add-ons |
| `Contract` | Month-to-month, one year, two year |
| `MonthlyCharges`, `TotalCharges` | Billing |
| `Churn` | Target - Yes / No |

`TotalCharges` has 11 blank entries for `tenure = 0` customers; these are coerced to `0.0`.

---

## Pipeline

```
python main.py
 ├── [1] db_setup.py        -> Load CSV into SQLite (schema-aware, idempotent)
 ├── [2] sql_analysis.py    -> KPI queries: churn rates, charge comparisons
 ├── [3] data_loader.py     -> Pull customers table into pandas
 ├── [4] create_features.py -> Encode target, one-hot categoricals, cast to float64
 ├── [5] churn_model.py     -> Logistic regression: train, evaluate, score all customers
 └── [6] visualization.py   -> Five production-quality charts saved to outputs/
```

---

## Project Structure

```
Customer-Behavior-Analysis/
├── data/
│   └── telco-customer-churn.csv
├── database/
│   └── churn.db
├── notebooks/
│   └── customer_churn_analysis.ipynb
├── outputs/                        # generated charts
├── src/
│   ├── churn_model.py
│   ├── create_features.py
│   ├── data_loader.py
│   ├── db_setup.py
│   ├── sql_analysis.py
│   └── visualization.py
├── main.py
└── README.md
```

---

## Step-by-Step Breakdown

### 1. Database Setup - `db_setup.py`

Loads the raw CSV into SQLite - not for performance, but to mirror production analytics environments where data lives in a relational store and downstream steps query it via SQL.

- 21 columns selected deliberately (schema design, not a `SELECT *`)
- `TotalCharges` coerced to numeric; blanks filled with `0.0` for `tenure = 0` rows
- `if_exists='replace'` makes the pipeline fully idempotent

### 2. SQL Analysis - `sql_analysis.py`

Four KPI queries answer the initial business questions before any ML:

| Query | Result |
|-------|--------|
| Overall churn rate | **26.5%** of 7,043 customers churned |
| Churn by contract | Month-to-month: **42.7%** · One year: **11.3%** · Two year: **2.8%** |
| Churn by internet service | Fiber optic: **41.9%** · DSL: **19.0%** · No internet: **7.4%** |
| Avg monthly charges | Churned: **$74.44** · Active: **$61.27** |

The last row raises an immediate question: do higher prices *cause* churn? The confounding analysis in Step 3 answers this directly.

### 3. Data Loading - `data_loader.py`

Pulls the full `customers` table into a pandas DataFrame. All downstream steps share this single source - no risk of divergence between what SQL sees and what the model trains on.

A confounding analysis runs immediately after loading, before any feature engineering touches the data.

### 4. Feature Engineering - `create_features.py`

Transforms raw data into a numeric feature matrix:

- Target encoding: `Churn` Yes/No -> 1/0
- `customerID` dropped (identifier, not a predictor)
- All categorical columns one-hot encoded via `pd.get_dummies(drop_first=True)`
- Full matrix cast to `float64`

Result: 30 numeric features from 21 raw columns.

### 5. Churn Risk Model - `churn_model.py`

Logistic Regression was chosen deliberately over ensemble methods for this stage:

- Outputs calibrated probabilities (critical for risk scoring, not just classification)
- Coefficients are directly interpretable as feature-level evidence
- Strong baseline: ROC-AUC ~0.84 on a stratified 80/20 split

**Key implementation decisions:**
- `stratify=y` in `train_test_split` - the dataset is imbalanced (26.5% churn); without stratification, a random split could under-represent churners in the test set and distort AUC
- `StandardScaler` fit only on training data, applied to test - no data leakage
- `solver='liblinear'` - avoids numerical overflow on older NumPy builds

**Evaluation:**

```
ROC-AUC: ~0.84

              precision    recall  f1-score
    Active        0.85      0.91      0.88
   Churned        0.69      0.56      0.62
```

Recall on the churned class (0.56) reflects the inherent imbalance. The probability scores - not the binary predictions - are what retention teams use. Customers with score > 0.5 are flagged for outreach.

**Top churn drivers (logistic regression coefficients):**

| Feature | Direction | Interpretation |
|---------|-----------|----------------|
| `tenure` | Negative | Longer tenure -> much lower churn risk |
| `InternetService_Fiber optic` | Positive | Fiber optic -> highest single driver of churn |
| `Contract_Two year` | Negative | Two-year contract -> strongly protective |
| `Contract_One year` | Negative | One-year -> moderately protective |
| `MonthlyCharges` | **Negative** | After controlling for contract + service, higher charges -> *slightly lower* risk |

The negative coefficient on `MonthlyCharges` is the most important number in this table. It directly contradicts the naive SQL observation that churned customers pay more. See the critical analysis below.

### 6. Visualization - `visualization.py`

Five charts saved to `outputs/`:

| File | Description |
|------|-------------|
| `churn_distribution.png` | Raw counts: active vs. churned |
| `churn_by_contract.png` | Churn rate by contract type |
| `churn_by_internet.png` | Churn rate by internet service |
| `monthly_charges_vs_churn.png` | Average monthly charge by churn status |
| `probability_distribution.png` | Predicted probability distributions - active vs. churned overlay |

Colour palette: dark green `#285700` (active) · blue `#1871BA` (churned).

---

## Outputs

<table>
  <tr>
    <td><img src="outputs/churn_by_contract.png" width="100%"></td>
    <td><img src="outputs/churn_by_internet.png" width="100%"></td>
  </tr>
  <tr>
    <td><img src="outputs/churn_distribution.png" width="100%"></td>
    <td><img src="outputs/monthly_charges_vs_churn.png" width="100%"></td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <img src="outputs/probability_distribution.png" width="100%">
    </td>
  </tr>
</table>

---

## Critical Analysis - Correlation vs. Causation

### The Misleading Observation

The SQL output shows churned customers pay **$13.17/month more** on average. The obvious conclusion - that high prices drive churn - is wrong, and acting on it (discounting bills) would waste retention budget.

### Why It's a Confounding Effect

Three variables co-move in this dataset:

**1. Contract type dominates churn**

Month-to-month customers churn at **42.7%**. Two-year customers churn at **2.8%** - a 15× difference. 88.6% of all churners were on month-to-month contracts. Month-to-month plans also carry higher monthly charges than annual plans, which is why churned customers *appear* to pay more.

**2. Fiber optic amplifies risk**

Fiber optic customers churn at **41.9%** vs. 19.0% for DSL. Fiber plans are more expensive than DSL, adding a second pricing confound. 69.4% of all churners were fiber optic customers.

The worst-performing segment - month-to-month + fiber optic - churns at **54.6%** and represents 30.2% of the customer base.

**3. Tenure is the leading indicator**

| Tenure | Churn Rate |
|--------|------------|
| 0–12 months | **47.7%** |
| 12–24 months | 28.7% |
| 24–48 months | 20.4% |
| 48–72 months | 9.5% |

55.5% of all churners left within their first 12 months. Median tenure for churned customers is **10 months** vs. 38 months for active customers. New customers are simultaneously more likely to be on month-to-month contracts, fiber plans, and paying higher rates - which is why all three correlate with churn in a univariate view.

**4. The model confirms it**

Within a controlled logistic regression, the coefficient for `MonthlyCharges` is **negative**. Holding contract type and service constant, a higher bill is weakly associated with *lower* churn risk - consistent with higher-value customers having more to lose by switching. Price is not the mechanism; it's a side-effect of the customer profile.

---

## Key Insights

- **The highest-risk customers share a profile, not just a price.** Month-to-month contract + fiber optic service + tenure under 12 months = 54.6% churn rate. This is a definable, targetable segment.
- **Contract type is the primary structural driver.** The gap between month-to-month (42.7%) and two-year (2.8%) churn is larger than any other split in the data. Switching a customer from month-to-month to annual is the highest-leverage intervention.
- **Fiber optic has a service quality problem.** Fiber customers churn at more than twice the DSL rate and pay more per month. Even on two-year contracts, fiber churn (7.2%) is nearly 4× higher than DSL on two-year (1.9%). This is not explained by price - it points to unmet expectations or service reliability issues.
- **MonthlyCharges is a proxy, not a cause.** Acting on price - through discounts or bill credits - treats the symptom rather than the disease. The real levers are contract structure and service experience.
- **Churn is front-loaded.** Nearly half of all churners leave within 12 months. Retention programs targeting this window would recover more than half the lost customers.

---

## Business Recommendations

These recommendations follow directly from the drivers identified above - not from the misleading raw correlation.

**1. Convert month-to-month customers to annual contracts in months 3–6.**
This is the single highest-impact lever. A 1-year contract reduces churn risk from 42.7% to 11.3%. Offer a meaningful incentive (waived setup fee, first month free) before the 12-month window closes - 55% of churners leave before they reach it.

**2. Investigate fiber optic service quality before expanding it.**
A 54.6% churn rate among the month-to-month fiber segment is a product problem. Before discounting fiber plans, audit support tickets, outage frequency, and speed consistency for this cohort. The issue is likely expectation vs. delivery, not price.

**3. Build an early-tenure engagement program.**
Flag all customers under 12 months with a model score > 0.5 for proactive outreach - a check-in call, a usage review, an educational email sequence. This cohort generates 55.5% of all churn and is the most cost-effective place to intervene.

**4. Do not use bill discounting as a retention tactic.**
The model shows that `MonthlyCharges` is a negative predictor of churn once segment is controlled for. Discounting reduces margin without addressing the structural drivers. Customers who churn because of contract flexibility or service dissatisfaction will not be retained by a 10% bill credit.

**5. Use the risk score to prioritise, not just flag.**
Customers with a predicted churn probability > 0.7 represent the highest-confidence targets. Prioritise outreach here, then work down the score distribution based on retention capacity.

---

## Technologies

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| pandas | Data manipulation and SQL result handling |
| NumPy | Numerical operations |
| scikit-learn | Model training, scaling, evaluation |
| matplotlib | Visualizations |
| SQLite / sqlite3 | Lightweight relational database |
| Jupyter Notebook | Interactive exploration |

---

## How to Run

```bash
# 1. Clone and navigate
git clone <repo-url>
cd Customer-Behavior-Analysis

# 2. Install dependencies
pip3 install pandas scikit-learn matplotlib notebook ipykernel --break-system-packages

# 3. Add the dataset
# Download telco-customer-churn.csv from Kaggle and place in data/

# 4. Run the full pipeline
python main.py
# -> outputs/ for charts, database/churn.db for the SQLite database

# 5. Or explore interactively
jupyter notebook notebooks/customer_churn_analysis.ipynb
```

---

## Future Improvements

- **XGBoost / Random Forest** - Ensemble methods would likely improve recall on the churned class (currently 0.56), which is the model's weakest dimension.
- **SHAP values** - Per-customer feature attribution would make the risk scores explainable to non-technical stakeholders and support individual retention decisions.
- **Streamlit dashboard** - Connecting the SQLite output to an interactive app would enable self-serve exploration and real-time scoring for the retention team.
- **Automated retraining** - Scheduling the pipeline on monthly data exports and monitoring for model drift as customer mix evolves over time.