import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import COLORS, apply_layout, classify_emitter

# Retrieve shared data from session state
country_df = st.session_state.country_df
country_co2 = st.session_state.country_co2
selected_country = st.session_state.selected_country
year_range = st.session_state.year_range

st.markdown('<div class="section-title"><span class="icon">📈</span> Historical CO₂ Emissions</div>', unsafe_allow_html=True)

chart_type = st.radio("Chart type", ["Line", "Area", "Bar", "Scatter"], horizontal=True, label_visibility="collapsed")

if chart_type == "Line":
    fig = px.line(country_co2, x="year", y="co2", color_discrete_sequence=[COLORS[0]])
    fig.update_traces(line=dict(width=2.5), mode="lines")
elif chart_type == "Area":
    fig = px.area(country_co2, x="year", y="co2", color_discrete_sequence=[COLORS[0]])
    fig.update_traces(line=dict(width=2), fillcolor="rgba(108,99,255,0.15)")
elif chart_type == "Bar":
    fig = px.bar(country_co2, x="year", y="co2", color_discrete_sequence=[COLORS[0]])
    fig.update_traces(marker=dict(cornerradius=3))
else:
    fig = px.scatter(country_co2, x="year", y="co2", color_discrete_sequence=[COLORS[0]], size="co2",
                     size_max=18, opacity=0.7)

fig.update_layout(xaxis_title="Year", yaxis_title="CO₂ Emissions (Million Tonnes)")
apply_layout(fig, f"{selected_country} — CO₂ Emissions ({year_range[0]}–{year_range[1]})")
st.plotly_chart(fig, use_container_width=True)

# YoY Growth Rate
st.markdown('<div class="section-title"><span class="icon">📊</span> Year-over-Year Growth Rate</div>', unsafe_allow_html=True)

growth_df = country_df[["year", "co2_growth_prct"]].dropna()
if not growth_df.empty:
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(
        x=growth_df["year"],
        y=growth_df["co2_growth_prct"],
        marker_color=[COLORS[4] if v < 0 else COLORS[3] for v in growth_df["co2_growth_prct"]],
        marker=dict(cornerradius=2),
    ))
    fig_growth.update_layout(xaxis_title="Year", yaxis_title="Growth Rate (%)")
    fig_growth.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.2)")
    apply_layout(fig_growth, f"{selected_country} — Annual CO₂ Growth Rate", height=350)
    st.plotly_chart(fig_growth, use_container_width=True)
else:
    st.info("Growth rate data not available for this country.")

# Emission level info
peak_co2 = country_co2["co2"].max()
level_label, _, level_desc = classify_emitter(peak_co2)

with st.expander(f"ℹ️ Emission Classification: {level_label}"):
    st.markdown(f"**{level_desc}**")
    st.markdown("""
    **Understanding CO₂ Metrics:**
    - **MtCO₂** — Million Metric Tonnes of Carbon Dioxide
    - **Per Capita** — Tonnes of CO₂ per person per year
    - **Global Share** — Percentage of worldwide CO₂ emissions

    **Why CO₂ Levels Matter:**
    - 🌡️ Accelerates global warming and climate change
    - 🔥 Triggers extreme heatwaves, wildfires, and droughts
    - 🌊 Causes sea level rise and stronger hurricanes
    - 💨 Contributes to air pollution and respiratory health issues
    - 🌾 Impacts agriculture, food supply, and water sources
    - 🐟 Causes ocean acidification, harming marine ecosystems
    """)
