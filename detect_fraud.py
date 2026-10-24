"""Detect sudden drops in consumption (fraud/bypass)."""
import pandas as pd
import numpy as np

def detect_fraud(csv_path="data.csv"):
    df = pd.read_csv(csv_path)
    df = df.sort_values(["customer_id", "month"])
    
    # 1. Calculate the historical average (the "baseline")
    # We use shift(1) so a customer isn't compared to their own current month
    df["rolling_avg_past"] = df.groupby("customer_id")["kwh_consumed"].transform(
        lambda x: x.shift(1).rolling(window=6, min_periods=3).mean()
    )
    
    # 2. Calculate the ratio of current usage to past usage
    df["usage_ratio"] = df["kwh_consumed"] / df["rolling_avg_past"]
    
    # 3. Flag if usage drops below 25% of their historical average
    # (Also ensure their past average was at least 20 kWh to avoid false alarms on tiny users)
    df["fraud_flag"] = (
        (df["usage_ratio"] < 0.25) & 
        (df["rolling_avg_past"] > 20)
    ).astype(int)
    
    # 4. Only alert if the drop is sustained for 2 consecutive months
    # (e.g. they didn't just go on holiday for one month)
    df["sustained_fraud"] = df.groupby("customer_id")["fraud_flag"].transform(
        lambda x: x.rolling(window=2).sum() == 2
    ).astype(int)
    
    return df

if __name__ == "__main__":
    results = detect_fraud()
    
    # Filter to just the flagged rows
    alerts = results[results["sustained_fraud"] == 1]
    
    # Get unique customers flagged
    unique_flagged = alerts["customer_id"].nunique()
    actual_fraudsters = results[results["is_fraud_ground_truth"] == 1]["customer_id"].nunique()
    
    print(f"=== FRAUD DETECTION RESULTS ===")
    print(f"Total Customers: 1000")
    print(f"Actual Fraudsters: {actual_fraudsters}")
    print(f"Customers Flagged by System: {unique_flagged}")
    
    print("\nSample Alerts:")
    print(alerts[["customer_id", "month", "kwh_consumed", "rolling_avg_past", "usage_ratio"]].head())
    
    # Save to CSV
    alerts.to_csv("fraud_alerts.csv", index=False)
    print(f"\nSaved {len(alerts)} alerts to fraud_alerts.csv")
