import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Retail Surge & Dynamic Inventory Pricing Engine",
    page_icon="⚡",
    layout="wide"
)

# --- HEADER SECTION ---
st.title("⚡ Retail Surge & Dynamic Inventory Pricing Engine")
st.markdown("Algorithmic dynamic pricing model balancing inventory depletion, demand shocks, and margin capture.")

# --- SIDEBAR: CONTROLS & HYPERPARAMETERS ---
st.sidebar.header("🛠️ Simulation Controls")

base_price = st.sidebar.slider(
    "Base Unit Price ($)", 
    min_value=10.0, 
    max_value=250.0, 
    value=50.0, 
    step=1.0
)

inventory_stock = st.sidebar.slider(
    "Available Inventory Stock (Units)", 
    min_value=10, 
    max_value=500, 
    value=120, 
    step=5
)

demand_multiplier = st.sidebar.slider(
    "Real-time Demand Shock (x Normal)", 
    min_value=0.5, 
    max_value=3.5, 
    value=1.8, 
    step=0.1
)

surge_sensitivity = st.sidebar.slider(
    "Surge Algorithm Sensitivity (α)", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.45, 
    step=0.05
)

competitor_price = st.sidebar.number_input(
    "Competitor Anchor Price ($)", 
    value=55.0, 
    step=1.0
)

# --- CORE ALGORITHM COMPUTATION ---
scarcity_factor = max(0.0, (200 - inventory_stock) / 200)
calculated_surge_rate = 1.0 + ((demand_multiplier - 1.0) * surge_sensitivity) + (scarcity_factor * 0.25)
dynamic_price = round(base_price * calculated_surge_rate, 2)

cogs = base_price * 0.60
unit_margin = round(dynamic_price - cogs, 2)
margin_percentage = round((unit_margin / dynamic_price) * 100, 1)

demand_elasticity = demand_multiplier / (calculated_surge_rate ** 1.2)
est_sales_units = int(max(5, min(inventory_stock, (inventory_stock * 0.75) * demand_elasticity)))
projected_revenue = round(est_sales_units * dynamic_price, 2)

# --- TOP EXECUTIVE METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    label="Dynamic Surge Price", 
    value=f"${dynamic_price}", 
    delta=f"{round(dynamic_price - base_price, 2)} vs Base"
)
col2.metric(
    label="Projected Revenue", 
    value=f"${projected_revenue:,.2f}"
)
col3.metric(
    label="Estimated Sales Volume", 
    value=f"{est_sales_units} units", 
    delta=f"{inventory_stock - est_sales_units} remaining", 
    delta_color="inverse"
)
col4.metric(
    label="Unit Margin ($)", 
    value=f"${unit_margin}", 
    delta=f"{margin_percentage}% Margin"
)

st.divider()

# --- CHART: REAL-TIME ELASTICITY & REVENUE CURVE ---
st.subheader("📈 Real-Time Price Elasticity & Revenue Surface")

price_range = np.linspace(base_price * 0.6, base_price * 2.5, 50)
simulated_demand = np.maximum(5, (inventory_stock * 1.4) / (1 + np.exp(0.07 * (price_range - competitor_price))))
simulated_rev = price_range * simulated_demand

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=price_range, 
    y=simulated_rev, 
    mode='lines', 
    name='Projected Revenue ($)', 
    line=dict(color='#00CC96', width=3)
))
fig.add_trace(go.Scatter(
    x=price_range, 
    y=simulated_demand, 
    mode='lines', 
    name='Units Demanded', 
    yaxis='y2', 
    line=dict(color='#636EFA', dash='dash', width=2)
))

fig.add_vline(
    x=dynamic_price, 
    line_width=2, 
    line_dash="dot", 
    line_color="#EF553B", 
    annotation_text=f"Active Price: ${dynamic_price}",
    annotation_position="top left"
)

fig.update_layout(
    xaxis_title="Unit Price ($)",
    yaxis=dict(title="Projected Revenue ($)", side="left"),
    yaxis2=dict(title="Units Demanded", overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.98),
    margin=dict(l=20, r=20, t=30, b=20),
    template="plotly_white",
    height=420
)
st.plotly_chart(fig, use_container_width=True)

# --- SCENARIO BENCHMARK TABLE ---
st.subheader("📋 Algorithmic Scenario Stress Test")
scenarios_df = pd.DataFrame({
    "Market Condition": [
        "Normal Trading Hour", 
        "Moderate Traffic Spike", 
        "Current Simulation", 
        "Competitor Stockout Shock", 
        "Extreme Flash Demand"
    ],
    "Demand Multiplier": [1.0, 1.3, demand_multiplier, 2.2, 3.2],
    "Engine Price ($)": [
        base_price, 
        round(base_price * 1.15, 2), 
        dynamic_price, 
        round(base_price * 1.65, 2), 
        round(base_price * 2.30, 2)
    ],
    "Depletion Estimate": [
        "20%", 
        "40%", 
        f"{round((est_sales_units / inventory_stock) * 100)}%", 
        "85%", 
        "98%"
    ],
    "Intervention State": [
        "Standard Baseline", 
        "Optimized", 
        "Active Simulation", 
        "Surge Guardrail Active", 
        "Cap Limit Triggered"
    ]
})
st.dataframe(scenarios_df, use_container_width=True)
