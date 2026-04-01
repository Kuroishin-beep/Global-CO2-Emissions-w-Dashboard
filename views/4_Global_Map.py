import streamlit as st
import plotly.express as px
from utils.helpers import PLOTLY_LAYOUT

df = st.session_state.df

st.markdown('<div class="section-title"><span class="icon">🗺️</span> Global CO₂ Emissions Map</div>', unsafe_allow_html=True)

map_metric = st.radio("Map metric", ["Total CO₂ (Mt)", "Per Capita (t)", "Global Share (%)"], horizontal=True)
map_year = st.select_slider("Select year", options=sorted(df["year"].dropna().unique().astype(int)),
                                value=min(2022, int(df["year"].max())))

col_map = {"Total CO₂ (Mt)": "co2", "Per Capita (t)": "co2_per_capita", "Global Share (%)": "share_global_co2"}
metric_col = col_map[map_metric]

map_df = df[df["year"] == map_year][["country", "iso_code", metric_col]].dropna()
map_df = map_df[map_df["iso_code"].notna() & (map_df["iso_code"].str.len() == 3)]

if not map_df.empty:
    fig_map = px.choropleth(
        map_df,
        locations="iso_code",
        color=metric_col,
        hover_name="country",
        color_continuous_scale=["#0E1117", "#06B6D4", "#6C63FF", "#F59E0B", "#EF4444"],
        labels={metric_col: map_metric},
    )
    fig_map.update_geos(
        showcoastlines=True, coastlinecolor="rgba(108,99,255,0.3)",
        showland=True, landcolor="#1A1D29",
        showocean=True, oceancolor="#0E1117",
        showlakes=False,
        showcountries=True, countrycolor="rgba(108,99,255,0.15)",
        bgcolor="rgba(0,0,0,0)",
        projection_type="natural earth",
    )
    fig_map.update_layout(
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis"]},
        height=550,
        coloraxis_colorbar=dict(
            title=dict(text=map_metric, font=dict(size=12)),
            thicknessmode="pixels", thickness=12,
            lenmode="fraction", len=0.7,
            tickfont=dict(size=10),
        ),
        geo=dict(
            showframe=False,
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Top emitters table
    st.markdown(f'<div class="section-title"><span class="icon">🏆</span> Top 15 Emitters — {map_year}</div>', unsafe_allow_html=True)
    top_df = map_df.nlargest(15, metric_col)[["country", metric_col]].reset_index(drop=True)
    top_df.index = top_df.index + 1
    top_df.columns = ["Country", map_metric]
    st.dataframe(top_df, use_container_width=True)
else:
    st.warning(f"No map data available for year {map_year}.")
