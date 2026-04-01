import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import COLORS, apply_layout

country_df = st.session_state.country_df

st.markdown('<div class="section-title"><span class="icon">⛽</span> Emission Breakdown by Source</div>', unsafe_allow_html=True)

source_cols = {"coal_co2": "Coal", "oil_co2": "Oil", "gas_co2": "Gas", "cement_co2": "Cement"}
source_data = country_df[["year"] + list(source_cols.keys())].dropna(subset=list(source_cols.keys()), how="all")

if not source_data.empty:
    source_data = source_data.fillna(0)

    col1, col2 = st.columns(2)

    with col1:
        # Stacked area
        fig_stack = go.Figure()
        for i, (col, name) in enumerate(source_cols.items()):
            fig_stack.add_trace(go.Scatter(
                x=source_data["year"], y=source_data[col],
                name=name, stackgroup="one",
                line=dict(width=0.5, color=COLORS[i]),
                fillcolor=COLORS[i].replace(")", ",0.4)").replace("rgb", "rgba") if "rgb" in COLORS[i] else COLORS[i],
            ))
        fig_stack.update_layout(xaxis_title="Year", yaxis_title="CO₂ (Mt)")
        apply_layout(fig_stack, "Stacked Emission Sources Over Time", height=400)
        st.plotly_chart(fig_stack, use_container_width=True)

    with col2:
        # Pie chart - latest year
        latest_sources = source_data.iloc[-1]
        pie_data = pd.DataFrame({
            "Source": list(source_cols.values()),
            "CO₂ (Mt)": [latest_sources[c] for c in source_cols.keys()],
        })
        pie_data = pie_data[pie_data["CO₂ (Mt)"] > 0]

        fig_pie = px.pie(pie_data, values="CO₂ (Mt)", names="Source", color_discrete_sequence=COLORS,
                         hole=0.45)
        fig_pie.update_traces(textposition="inside", textinfo="percent+label",
                              textfont_size=12)
        apply_layout(fig_pie, f"Source Mix — Latest Year ({int(latest_sources['year'])})", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Individual source trends
    st.markdown('<div class="section-title"><span class="icon">📉</span> Individual Source Trends</div>', unsafe_allow_html=True)
    src_cols = st.columns(4)
    for i, (col, name) in enumerate(source_cols.items()):
        with src_cols[i]:
            fig_mini = px.area(source_data, x="year", y=col, color_discrete_sequence=[COLORS[i]])
            fig_mini.update_traces(line=dict(width=1.5))
            apply_layout(fig_mini, name, height=220)
            fig_mini.update_layout(
                margin=dict(l=20, r=10, t=35, b=30),
                showlegend=False,
                xaxis=dict(title=""),
                yaxis=dict(title=""),
            )
            st.plotly_chart(fig_mini, use_container_width=True)
else:
    st.info("Source breakdown data not available for this country.")
