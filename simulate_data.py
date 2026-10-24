"""Simulate KPLC meter readings with hidden fraud cases."""
import numpy as np
import pandas as pd
from pathlib import Path

def generate():
    np.random.seed(42)
    n_customers = 1000
    months = 12
    
    # 5% of customers will commit fraud (bypass meter/move out)
    fraud_ids = np.random.choice(n_customers, size=50, replace=False)
    
    records = []
    for cust_id in range(n_customers):
        # Normal usage is around 100 kWh/month with some noise
        base_usage = np.random.normal(100, 15, months)
        
        if cust_id in fraud_ids:
            # Fraud starts at month 8. Usage drops by 85%
            fraud_start = 7 
            base_usage[fraud_start:] = base_usage[fraud_start:] * 0.15
            
        for month_idx in range(months):
            records.append({
                "customer_id": f"CUST_{cust_id:04d}",
                "month": month_idx + 1,
                "kwh_consumed": max(0, round(base_usage[month_idx], 2)),
                "is_fraud_ground_truth": int(cust_id in fraud_ids and month_idx >= 7)
            })
            
    df = pd.DataFrame(records)
    df.to_csv("data.csv", index=False)
    print(f"Generated {len(df)} rows for {n_customers} customers.")
    print(f"Total fraud cases injected: {len(fraud_ids)}")

if __name__ == "__main__":
    generate()