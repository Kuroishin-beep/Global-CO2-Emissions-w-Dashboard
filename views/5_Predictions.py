import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.helpers import COLORS, apply_layout, predict_emissions

country_df = st.session_state.country_df
country_co2 = st.session_state.country_co2
selected_country = st.session_state.selected_country

st.markdown('<div class="section-title"><span class="icon">🔮</span> Emission Forecasting</div>', unsafe_allow_html=True)

pred_df = predict_emissions(country_df)

if not pred_df.empty:
    r2 = pred_df["r2_score"].iloc[0]

    # Combine historical + predicted
    hist_tail = country_co2.tail(20).copy()
    hist_tail = hist_tail.rename(columns={"co2": "value"})
    hist_tail["type"] = "Historical"

    pred_plot = pred_df[["year", "predicted_co2"]].copy()
    pred_plot = pred_plot.rename(columns={"predicted_co2": "value"})
    pred_plot["type"] = "Predicted"

    combined = pd.concat([hist_tail, pred_plot])

    fig_pred = go.Figure()

    # Historical line
    fig_pred.add_trace(go.Scatter(
        x=hist_tail["year"], y=hist_tail["value"],
        name="Historical", mode="lines+markers",
        line=dict(color=COLORS[0], width=2.5),
        marker=dict(size=5),
    ))

    # Connection line
    connect_yr = hist_tail.iloc[-1]["year"]
    connect_val = hist_tail.iloc[-1]["value"]
    first_pred_yr = pred_plot.iloc[0]["year"]
    first_pred_val = pred_plot.iloc[0]["value"]
    fig_pred.add_trace(go.Scatter(
        x=[connect_yr, first_pred_yr],
        y=[connect_val, first_pred_val],
        mode="lines",
        line=dict(color=COLORS[1], width=2, dash="dot"),
        showlegend=False,
    ))

    # Prediction line
    fig_pred.add_trace(go.Scatter(
        x=pred_plot["year"], y=pred_plot["value"],
        name="Predicted", mode="lines+markers",
        line=dict(color=COLORS[1], width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"),
    ))

    # Add uncertainty band
    upper = pred_plot["value"] * (1 + (1 - r2) * 1.5)
    lower = np.maximum(pred_plot["value"] * (1 - (1 - r2) * 1.5), 0)
    fig_pred.add_trace(go.Scatter(
        x=pd.concat([pred_plot["year"], pred_plot["year"][::-1]]),
        y=pd.concat([upper, lower[::-1]]),
        fill="toself",
        fillcolor="rgba(6,182,212,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Uncertainty Range",
    ))

    fig_pred.update_layout(xaxis_title="Year", yaxis_title="CO₂ (Mt)")
    apply_layout(fig_pred, f"{selected_country} — CO₂ Forecast (Linear Regression)", height=450)
    st.plotly_chart(fig_pred, use_container_width=True)

    # Model info
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{r2:.4f}</div>
            <div class="metric-label">R² Score (Model Fit)</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        trend_dir = "📈 Increasing" if pred_df["predicted_co2"].iloc[-1] > pred_df["predicted_co2"].iloc[0] else "📉 Decreasing"
        change_pct = ((pred_df["predicted_co2"].iloc[-1] - pred_df["predicted_co2"].iloc[0]) / pred_df["predicted_co2"].iloc[0] * 100)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{trend_dir}</div>
            <div class="metric-label">Trend Direction ({change_pct:+.1f}% by 2050)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Prediction table
    with st.expander("📋 Forecast Data Table"):
        display_pred = pred_df[["year", "predicted_co2"]].copy()
        display_pred.columns = ["Year", "Predicted CO₂ (Mt)"]
        display_pred["Predicted CO₂ (Mt)"] = display_pred["Predicted CO₂ (Mt)"].round(2)
        st.dataframe(display_pred, use_container_width=True, hide_index=True)

    st.caption("⚠️ Predictions use a simple linear regression model and should be interpreted as trend indicators, not precise forecasts.")
else:
    st.warning("Not enough data to generate predictions for this country.")
