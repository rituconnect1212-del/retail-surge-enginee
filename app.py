import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- PAGE SETUP & THEME ---
st.set_page_config(
    page_title="Retail Surge & Dynamic Pricing Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished Executive UI
st.markdown("""
    <style>
    .main {
        background-color: #fcfcfd;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .badge-blue { background-color: #e0f2fe; color: #0369a1; }
    .badge-green { background-color: #dcfce7; color: #15803d; }
    .badge-orange { background-color: #ffedd5; color: #c2410c; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("⚡ Retail Surge & Dynamic Inventory Pricing Engine")
st.caption("Algorithmic decision-support system balancing dark-store inventory depletion, hyper-local demand shocks, and margin capture.")

# --- SIDEBAR: SIMULATION PARAMETERS ---
with st.sidebar:
    st.header("⚙️ Simulation Controls")
    
    # Preset Selector
    category_preset = st.selectbox(
        "Product Category Preset",
        ["Quick-Commerce Essentials (Milk/Bread)", "FMCG & Packaged Snacks", "Electronics & High-Value Retail"]
    )
    
    if category_preset == "Quick-Commerce Essentials (Milk/Bread)":
        default_base, default_stock, default_cogs_ratio = 60.0, 150, 0.75
    elif category_preset == "FMCG & Packaged Snacks":
        default_base, default_stock, default_cogs_ratio = 140.0, 300, 0.60
    else:
        default_base, default_stock, default_cogs_ratio = 850.0, 80, 0.50

    st.subheader("📦 Inventory & Costing")
    base_price = st.number_input("Base Unit Price (₹)", value=default_base, min_value=10.0, max_value=10000.0, step=5.0)
    inventory_stock = st.slider("Dark-Store Available Stock (Units)", min_value=10, max_value=500, value=default_stock, step=5)
    competitor_price = st.number_input("Competitor Reference Benchmark (₹)", value=round(base_price * 1.05, 1), step=5.0)

    st.subheader("🌧️ Hyper-Local Shocks")
    market_condition = st.selectbox(
        "Environmental Scenario Trigger",
        ["Normal Operating Conditions", "Heavy Monsoon Rainstorm", "Peak Festival / Match Rush", "Rider & Delivery Fleet Deficit"]
    )
    
    # Multiplier based on environmental shocks
    shock_map = {
        "Normal Operating Conditions": 1.0,
        "Heavy Monsoon Rainstorm": 1.8,
        "Peak Festival / Match Rush": 2.2,
        "Rider & Delivery Fleet Deficit": 1.5
    }
    demand_multiplier = shock_map[market_condition]
    st.info(f"Demand Multiplier applied: **{demand_multiplier}x**")

    surge_sensitivity = st.slider("Surge Algorithm Sensitivity (α)", min_value=0.1, max_value=1.0, value=0.45, step=0.05)

# --- CORE ALGORITHM CALCULATIONS ---
# 1. Scarcity Penalty based on buffer threshold
scarcity_factor = max(0.0, (200 - inventory_stock) / 200)

# 2. Dynamic Surge Multiplier
calculated_surge_rate = 1.0 + ((demand_multiplier - 1.0) * surge_sensitivity) + (scarcity_factor * 0.25)
dynamic_price = round(base_price * calculated_surge_rate, 1)

# 3. Unit Economics
unit_cogs = round(base_price * default_cogs_ratio, 1)
unit_margin = round(dynamic_price - unit_cogs, 1)
margin_percentage = round((unit_margin / dynamic_price) * 100, 1)

# 4. Projected Demand Volume & Revenue
demand_elasticity = demand_multiplier / (calculated_surge_rate ** 1.3)
est_sales_units = int(max(5, min(inventory_stock, (inventory_stock * 0.75) * demand_elasticity)))
projected_revenue = round(est_sales_units * dynamic_price, 2)
projected_gross_profit = round(est_sales_units * unit_margin, 2)

# --- EXECUTIVE STRATEGY BADGE ---
if calculated_surge_rate > 1.35 and inventory_stock < 50:
    st.error("🚨 **CRITICAL INVENTORY ALERT:** Scarcity cap triggered. Aggressive dynamic surge applied to preserve dark-store stock integrity.")
elif calculated_surge_rate > 1.15:
    st.warning("⚡ **ACTIVE SURGE STATE:** Demand shock absorbed. Real-time margin expansion active while sustaining target throughput.")
else:
    st.success("✅ **STABLE EQUILIBRIUM:** Standard supply-demand parity. Maintaining baseline gross margin targets.")

# --- TOP EXECUTIVE METRICS ROW ---
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Optimized Surge Price", f"₹{dynamic_price:,.1f}", delta=f"₹{round(dynamic_price - base_price, 1)} vs Base")
col2.metric("Projected Gross Revenue", f"₹{projected_revenue:,.0f}")
col3.metric("Projected Gross Profit", f"₹{projected_gross_profit:,.0f}", delta=f"{margin_percentage}% Margin")
col4.metric("Estimated Sales Units", f"{est_sales_units} units", delta=f"{inventory_stock - est_sales_units} remaining", delta_color="inverse")
col5.metric("Unit Contribution Margin", f"₹{unit_margin}", delta=f"COGS: ₹{unit_cogs}")

st.divider()

# --- DUAL CHART VISUALIZATION ---
tab1, tab2 = st.tabs(["📈 Elasticity & Revenue Surface", "📊 Supply vs Demand Dynamics"])

with tab1:
    price_range = np.linspace(base_price * 0.6, base_price * 2.5, 60)
    simulated_demand = np.maximum(5, (inventory_stock * 1.5) / (1 + np.exp(0.06 * (price_range - competitor_price))))
    simulated_rev = price_range * simulated_demand

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=price_range, 
        y=simulated_rev, 
        mode='lines', 
        name='Projected Revenue (₹)', 
        line=dict(color='#0ea5e9', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=price_range, 
        y=simulated_demand, 
        mode='lines', 
        name='Units Demanded', 
        yaxis='y2', 
        line=dict(color='#8b5cf6', dash='dash', width=2)
    ))

    fig.add_vline(
        x=dynamic_price, 
        line_width=2, 
        line_dash="dot", 
        line_color="#ef4444", 
        annotation_text=f"Engine Price: ₹{dynamic_price}",
        annotation_position="top left"
    )

    fig.update_layout(
        title="Revenue vs Price Elasticity Frontier",
        xaxis_title="Unit Price (₹)",
        yaxis=dict(title="Total Projected Revenue (₹)", side="left"),
        yaxis2=dict(title="Projected Unit Demand", overlaying='y', side='right'),
        legend=dict(x=0.01, y=0.98),
        template="plotly_white",
        height=450,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Units Depleted (Sales)',
        x=['Inventory Trajectory'],
        y=[est_sales_units],
        marker_color='#3b82f6'
    ))
    fig_bar.add_trace(go.Bar(
        name='Remaining Safety Stock',
        x=['Inventory Trajectory'],
        y=[inventory_stock - est_sales_units],
        marker_color='#94a3b8'
    ))
    fig_bar.update_layout(
        barmode='stack',
        title="Stock Depletion vs Buffer Retention",
        yaxis_title="Units",
        template="plotly_white",
        height=450
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- EXECUTIVE SCENARIO STRESS TEST MATRIX ---
st.subheader("📋 Scenario Stress-Test Matrix")
scenarios_df = pd.DataFrame({
    "Operating Condition": [
        "Normal Trading Hour", 
        "Moderate Traffic Spike", 
        "Current Live Simulation", 
        "Competitor Stockout Crisis", 
        "Severe Flash Monsoon Spike"
    ],
    "Demand Multiplier": [1.0, 1.3, demand_multiplier, 2.0, 3.2],
    "Engine Price (₹)": [
        f"₹{base_price:.1f}", 
        f"₹{round(base_price * 1.15, 1):.1f}", 
        f"₹{dynamic_price:.1f}", 
        f"₹{round(base_price * 1.55, 1):.1f}", 
        f"₹{round(base_price * 2.25, 1):.1f}"
    ],
    "Depletion Rate": [
        "22%", 
        "38%", 
        f"{round((est_sales_units / inventory_stock) * 100)}%", 
        "78%", 
        "95%"
    ],
    "Algorithmic Action": [
        "Baseline Pricing", 
        "Micro-Surge (Yield Expansion)", 
        "Real-Time Dynamic Balancing", 
        "Scarcity Protection Guardrail", 
        "Regulatory Cap Active"
    ]
})
st.dataframe(scenarios_df, use_container_width=True)

# --- EXPORT REPORT BUTTON ---
csv = scenarios_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Scenario Benchmark Report (CSV)",
    data=csv,
    file_name="dynamic_pricing_scenario_report.csv",
    mime="text/csv"
)

