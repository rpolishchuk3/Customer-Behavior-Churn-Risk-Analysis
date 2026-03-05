import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report

from create_features import create_customer_features


def calculate_churn_risk(df):
    """
    Trains a Logistic Regression model on the feature matrix and returns predicted churn risk scores for all customers.
    """

    
    df = df.copy()

    y = df['Churn']
    X = df.drop(columns=['Churn']).fillna(0)

    print("Number of features:", X.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # liblinear: no matmul overflow on older numpy, and don't pass penalty
    # explicitly — let it use the default to avoid triggering the warning
    model = LogisticRegression(max_iter=2000, solver='liblinear', C=1.0)
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    print("\n=== ML Model Evaluation ===")
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    X_scaled_full = scaler.transform(X)
    df['churn_risk_score'] = model.predict_proba(X_scaled_full)[:, 1]

    return df[['Churn', 'churn_risk_score']]


def evaluate_churn_model(risk_scores_df):
    """
    Evaluates the churn risk model by comparing scores for active vs churned customers.
    """


    active = risk_scores_df[risk_scores_df['Churn'] == 0]
    churned = risk_scores_df[risk_scores_df['Churn'] == 1]

    avg_risk_active = active['churn_risk_score'].mean()
    avg_risk_churned = churned['churn_risk_score'].mean()

    print("\n=== Churn Risk Model Evaluation ===")
    print(f"Average risk score for active customers:  {avg_risk_active:.2f}")
    print(f"Average risk score for churned customers: {avg_risk_churned:.2f}")
    print(f"Difference: {abs(avg_risk_churned - avg_risk_active):.2f}")

    print(f"\nActive customers:  {len(active)}")
    print(f"Churned customers: {len(churned)}")


if __name__ == "__main__":
    raw = pd.read_csv("telco-customer-churn.csv")
    features = create_customer_features(raw)

    risk_scores = calculate_churn_risk(features)
    print("\nSample risk scores:")
    print(risk_scores.head(10))

    evaluate_churn_model(risk_scores)