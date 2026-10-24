# KPLC Fraud & Meter Bypass Detection

A rule-based and statistical anomaly detection system to identify suspected electricity theft (meter bypass) in Kenya Power (KPLC) consumers.

## How it Works
The engine calculates a **6-month rolling baseline** for every customer. If a customer's monthly consumption suddenly drops below **25% of their historical average** for **2 consecutive months**, the system raises a fraud alert.

## Features
- **Synthetic Data Generator**: Simulates 1,000 consumers with 5% injecting hidden meter bypasses.
- **Detection Engine**: Flags sudden, sustained drops in consumption.
- **Interactive Streamlit Dashboard**: Allows analysts to visually inspect flagged accounts against their historical baselines before dispatching field inspectors.

## Quickstart

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install pandas numpy matplotlib streamlit

python simulate_data.py        # generates data.csv
python detect_fraud.py         # outputs fraud_alerts.csv
streamlit run app.py           # opens the interactive dashboard"# kplc-fraud-detection" 
