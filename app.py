import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from detect_fraud import detect_fraud

# Set up the page
st.set_page_config(page_title="KPLC Fraud Detector", layout="wide")
st.title("⚡ KPLC Fraud & Bypass Detection")
st.write("This dashboard analyzes consumer usage patterns and flags sustained drops in consumption.")

# Load data (using Streamlit cache so it doesn't reload every click)
@st.cache_data
def load_data():
    df = detect_fraud()
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
show_only_alerts = st.sidebar.checkbox("Show only flagged customers", value=True)

# Get unique flagged customers
alerts_df = df[df["sustained_fraud"] == 1]
flagged_ids = alerts_df["customer_id"].unique()

if show_only_alerts:
    display_ids = flagged_ids
else:
    display_ids = df["customer_id"].unique()

# Dropdown to select a customer
selected_customer = st.selectbox(
    f"Select a Customer (Found {len(flagged_ids)} flagged)",
    options=display_ids
)

# Filter data for selected customer
cust_data = df[df["customer_id"] == selected_customer].sort_values("month")

# Layout: Two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Customer Details")
    st.write(f"**ID:** {selected_customer}")
    
    # Check if they are truly a fraudster in our simulation
    is_real_fraud = cust_data["is_fraud_ground_truth"].max()
    if is_real_fraud:
        st.error("🚨 Ground Truth: SIMULATED FRAUDSTER")
    else:
        st.success("✅ Ground Truth: NORMAL CONSUMER")
        
    # Show if our system flagged them
    is_flagged = cust_data["sustained_fraud"].max()
    if is_flagged:
        st.warning("⚠️ System Flag: ALERT ISSUED")
    else:
        st.info("System Flag: No Alert")

with col2:
    st.subheader("Consumption History (kWh)")
    
    # Plot the usage
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cust_data["month"], cust_data["kwh_consumed"], marker="o", label="Actual Usage", color="blue")
    ax.plot(cust_data["month"], cust_data["rolling_avg_past"], linestyle="--", label="6-Month Baseline", color="gray")
    
    # Highlight the alert area if flagged
    if is_flagged:
        alert_months = cust_data[cust_data["sustained_fraud"] == 1]["month"]
        ax.axvspan(alert_months.min() - 0.5, alert_months.max() + 0.5, color="red", alpha=0.1, label="Alert Period")
        
    ax.set_xlabel("Month")
    ax.set_ylabel("kWh Consumed")
    ax.legend()
    ax.grid(alpha=0.3)
    
    st.pyplot(fig)