import streamlit as st
import plotly.express as px
from utils.helpers import COLORS, apply_layout

df = st.session_state.df
selected_country = st.session_state.selected_country
compare_countries = st.session_state.compare_countries
year_range = st.session_state.year_range

st.markdown('<div class="section-title"><span class="icon">🔀</span> Country Comparison</div>', unsafe_allow_html=True)

all_compare = [selected_country] + compare_countries
if len(all_compare) < 2:
    st.info("Select at least one comparison country from the sidebar to enable this view.")
else:
    compare_df = df[df["country"].isin(all_compare) & df["year"].between(*year_range)].copy()
    compare_co2 = compare_df[["country", "year", "co2"]].dropna()

    col1, col2 = st.columns(2)

    with col1:
        # Total emissions comparison
        fig_comp = px.line(compare_co2, x="year", y="co2", color="country",
                           color_discrete_sequence=COLORS)
        fig_comp.update_traces(line=dict(width=2.5))
        fig_comp.update_layout(xaxis_title="Year", yaxis_title="CO₂ (Mt)")
        apply_layout(fig_comp, "Total CO₂ Emissions Comparison")
        st.plotly_chart(fig_comp, use_container_width=True)

    with col2:
        # Per capita
        compare_pc = compare_df[["country", "year", "co2_per_capita"]].dropna()
        if not compare_pc.empty:
            fig_pc = px.line(compare_pc, x="year", y="co2_per_capita", color="country",
                             color_discrete_sequence=COLORS)
            fig_pc.update_traces(line=dict(width=2.5))
            fig_pc.update_layout(xaxis_title="Year", yaxis_title="CO₂ per Capita (t)")
            apply_layout(fig_pc, "Per Capita Emissions Comparison")
            st.plotly_chart(fig_pc, use_container_width=True)
        else:
            st.info("Per capita data not available.")

    # Rankings bar chart
    st.markdown('<div class="section-title"><span class="icon">🏆</span> Latest Emissions Ranking</div>', unsafe_allow_html=True)
    latest_compare = compare_df.sort_values("year").groupby("country").last().reset_index()
    latest_compare = latest_compare[["country", "co2", "co2_per_capita"]].dropna(subset=["co2"])
    latest_compare = latest_compare.sort_values("co2", ascending=True)

    fig_rank = px.bar(latest_compare, x="co2", y="country", orientation="h",
                      color="co2", color_continuous_scale=["#06B6D4", "#6C63FF", "#EF4444"],
                      text=latest_compare["co2"].apply(lambda x: f"{x:,.1f} Mt"))
    fig_rank.update_traces(textposition="outside", textfont=dict(color="#A5A8BD"))
    fig_rank.update_layout(coloraxis_showscale=False, xaxis_title="CO₂ (Mt)", yaxis_title="")
    apply_layout(fig_rank, "Total Emissions — Latest Available Year", height=max(250, len(all_compare) * 55))
    st.plotly_chart(fig_rank, use_container_width=True)
