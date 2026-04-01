import streamlit as st
import pandas as pd
from utils.helpers import classify_emitter

def render_header():
    st.markdown("""
    <div class="dashboard-header">
        <h1>🌍 Global CO₂ Emissions Dashboard</h1>
        <p>Interactive analysis of worldwide carbon dioxide emissions — historical trends, forecasts, and deep analytics</p>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_metrics(df, selected_country, year_range):
    country_df = df[(df["country"] == selected_country) & (df["year"].between(*year_range))].copy()
    country_co2 = country_df[["year", "co2"]].dropna()

    if not country_co2.empty:
        latest_co2 = country_co2.iloc[-1]["co2"]
        peak_co2 = country_co2["co2"].max()
        peak_year = int(country_co2.loc[country_co2["co2"].idxmax(), "year"])
        avg_co2 = country_co2["co2"].mean()

        # YoY change
        if len(country_co2) >= 2:
            prev_co2 = country_co2.iloc[-2]["co2"]
            yoy_change = ((latest_co2 - prev_co2) / prev_co2 * 100) if prev_co2 != 0 else 0
        else:
            yoy_change = 0

        # Per capita
        latest_row = country_df.iloc[-1] if not country_df.empty else None
        per_capita = latest_row["co2_per_capita"] if latest_row is not None and pd.notna(latest_row.get("co2_per_capita")) else None
        share_global = latest_row["share_global_co2"] if latest_row is not None and pd.notna(latest_row.get("share_global_co2")) else None

        level_label, _, _ = classify_emitter(peak_co2)

        cols = st.columns(6)
        metrics = [
            (f"{latest_co2:,.1f}", "Latest CO₂ (Mt)", f"{'▲' if yoy_change > 0 else '▼'} {abs(yoy_change):.1f}% YoY", yoy_change > 0),
            (f"{peak_co2:,.1f}", "Peak CO₂ (Mt)", f"Year {peak_year}", None),
            (f"{avg_co2:,.1f}", "Average CO₂ (Mt)", f"{year_range[0]}–{year_range[1]}", None),
            (f"{per_capita:.2f}" if per_capita else "N/A", "Per Capita (t)", "Tonnes per person", None),
            (f"{share_global:.2f}%" if share_global else "N/A", "Global Share", "% of world emissions", None),
            (level_label.split(" ", 1)[1], "Emission Level", level_label.split(" ")[0], None),
        ]

        for i, (val, label, delta, is_up) in enumerate(metrics):
            with cols[i]:
                delta_class = "metric-delta-up" if is_up is True else ("metric-delta-down" if is_up is False else "metric-label")
                delta_html = f'<div class="{delta_class}">{delta}</div>' if delta else ""
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                    {delta_html}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("")
        return True, country_df, country_co2
    else:
        st.warning(f"No CO₂ data available for **{selected_country}** in the selected year range.")
        return False, None, None
