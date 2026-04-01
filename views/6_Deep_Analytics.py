import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import COLORS, apply_layout

country_df = st.session_state.country_df
selected_country = st.session_state.selected_country

st.markdown('<div class="section-title"><span class="icon">🧪</span> Deep Analytics</div>', unsafe_allow_html=True)

analytics_col1, analytics_col2 = st.columns(2)

# ── CO2 vs GDP ──
with analytics_col1:
    st.markdown("#### CO₂ vs GDP")
    gdp_data = country_df[["year", "co2", "gdp"]].dropna()
    if len(gdp_data) > 5:
        fig_gdp = px.scatter(gdp_data, x="gdp", y="co2", color="year",
                              color_continuous_scale=["#06B6D4", "#6C63FF"],
                              size="co2", size_max=15, opacity=0.7,
                              hover_data=["year"])
        # Trendline
        if len(gdp_data) > 3:
            z = np.polyfit(gdp_data["gdp"], gdp_data["co2"], 1)
            p = np.poly1d(z)
            x_line = np.linspace(gdp_data["gdp"].min(), gdp_data["gdp"].max(), 100)
            fig_gdp.add_trace(go.Scatter(x=x_line, y=p(x_line), mode="lines",
                                          line=dict(color="#F59E0B", dash="dash", width=2),
                                          name="Trend"))
        fig_gdp.update_layout(xaxis_title="GDP (USD)", yaxis_title="CO₂ (Mt)")
        apply_layout(fig_gdp, "Carbon Intensity vs Economic Output", height=380)
        st.plotly_chart(fig_gdp, use_container_width=True)

        corr = gdp_data["co2"].corr(gdp_data["gdp"])
        st.caption(f"Pearson Correlation: **{corr:.3f}** — {'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'} relationship")
    else:
        st.info("Not enough GDP data for this country.")

# ── CO2 vs Population ──
with analytics_col2:
    st.markdown("#### CO₂ vs Population")
    pop_data = country_df[["year", "co2", "population"]].dropna()
    if len(pop_data) > 5:
        pop_data["population_millions"] = pop_data["population"] / 1e6
        fig_pop = px.scatter(pop_data, x="population_millions", y="co2", color="year",
                              color_continuous_scale=["#06B6D4", "#6C63FF"],
                              size="co2", size_max=15, opacity=0.7,
                              hover_data=["year"])
        if len(pop_data) > 3:
            z = np.polyfit(pop_data["population_millions"], pop_data["co2"], 1)
            p = np.poly1d(z)
            x_line = np.linspace(pop_data["population_millions"].min(), pop_data["population_millions"].max(), 100)
            fig_pop.add_trace(go.Scatter(x=x_line, y=p(x_line), mode="lines",
                                          line=dict(color="#F59E0B", dash="dash", width=2),
                                          name="Trend"))
        fig_pop.update_layout(xaxis_title="Population (Millions)", yaxis_title="CO₂ (Mt)")
        apply_layout(fig_pop, "Emissions vs Population Growth", height=380)
        st.plotly_chart(fig_pop, use_container_width=True)

        corr = pop_data["co2"].corr(pop_data["population"])
        st.caption(f"Pearson Correlation: **{corr:.3f}** — {'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'} relationship")
    else:
        st.info("Not enough population data for this country.")

# ── GHG Composition ──
st.markdown('<div class="section-title"><span class="icon">🧬</span> Greenhouse Gas Composition</div>', unsafe_allow_html=True)
ghg_cols = {"co2": "CO₂", "methane": "Methane", "nitrous_oxide": "Nitrous Oxide"}
ghg_data = country_df[["year"] + list(ghg_cols.keys())].dropna(subset=list(ghg_cols.keys()), how="all").fillna(0)

if not ghg_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig_ghg = go.Figure()
        for i, (col, name) in enumerate(ghg_cols.items()):
            fig_ghg.add_trace(go.Scatter(
                x=ghg_data["year"], y=ghg_data[col],
                name=name, mode="lines",
                line=dict(width=2.5, color=COLORS[i]),
            ))
        fig_ghg.update_layout(xaxis_title="Year", yaxis_title="Emissions (Mt)")
        apply_layout(fig_ghg, "GHG Trends Over Time")
        st.plotly_chart(fig_ghg, use_container_width=True)

    with col2:
        latest_ghg = ghg_data.iloc[-1]
        ghg_pie = pd.DataFrame({
            "Gas": list(ghg_cols.values()),
            "Value": [latest_ghg[c] for c in ghg_cols.keys()],
        })
        ghg_pie = ghg_pie[ghg_pie["Value"] > 0]
        fig_ghg_pie = px.pie(ghg_pie, values="Value", names="Gas", color_discrete_sequence=COLORS, hole=0.45)
        fig_ghg_pie.update_traces(textposition="inside", textinfo="percent+label")
        apply_layout(fig_ghg_pie, f"GHG Mix — Year {int(latest_ghg['year'])}")
        st.plotly_chart(fig_ghg_pie, use_container_width=True)
else:
    st.info("No GHG composition data available for this country.")

# ── Temperature Contribution ──
st.markdown('<div class="section-title"><span class="icon">🌡️</span> Temperature Change Contribution</div>', unsafe_allow_html=True)
temp_data = country_df[["year", "temperature_change_from_co2", "temperature_change_from_ghg"]].dropna()
if not temp_data.empty:
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=temp_data["year"], y=temp_data["temperature_change_from_co2"],
        name="From CO₂", fill="tonexty" if "temperature_change_from_ghg" in temp_data else None,
        line=dict(color=COLORS[3], width=2),
    ))
    fig_temp.add_trace(go.Scatter(
        x=temp_data["year"], y=temp_data["temperature_change_from_ghg"],
        name="From All GHGs", fill="tonexty",
        line=dict(color=COLORS[5], width=2),
        fillcolor="rgba(236,72,153,0.1)",
    ))
    fig_temp.update_layout(xaxis_title="Year", yaxis_title="Temperature Change (°C)")
    apply_layout(fig_temp, f"{selected_country} — Contribution to Global Temperature Rise", height=380)
    st.plotly_chart(fig_temp, use_container_width=True)
else:
    st.info("Temperature contribution data not available for this country.")

# ── Statistical Summary ──
st.markdown('<div class="section-title"><span class="icon">📊</span> Statistical Summary</div>', unsafe_allow_html=True)
stat_cols = ["co2", "co2_per_capita", "coal_co2", "oil_co2", "gas_co2", "cement_co2", "population", "gdp"]
stat_available = [c for c in stat_cols if c in country_df.columns]
stats = country_df[stat_available].describe().round(2)
st.dataframe(stats, use_container_width=True)
