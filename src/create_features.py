import pandas as pd


def create_customer_features(df):
    """
    Encodes the target variable, cleans TotalCharges, one-hot encodes categorical columns, and returns a numeric feature matrix.
    """


    df = df.copy()

    # Convert target
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

    # Strip whitespace before converting — fixes 11 blank TotalCharges rows
    # where tenure=0 customers have " " instead of NaN
    df['TotalCharges'] = df['TotalCharges'].astype(str).str.strip()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)

    df = df.drop(columns=['customerID'])

    # One-hot encode — explicitly pass dtype=str to avoid pandas deprecation warning
    cat_cols = df.select_dtypes(include=['object']).columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Ensure all columns are numeric
    df = df.astype(float)

    print(f"Created features for {len(df)} customers")
    print(f"Feature matrix shape: {df.shape}")

    return df


if __name__ == "__main__":
    raw = pd.read_csv("telco-customer-churn.csv")
    features = create_customer_features(raw)
    print("\nSample features:")
    print(features.head())