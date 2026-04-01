import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.style import load_css
from components.metrics import render_header, render_kpi_metrics

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Global CO₂ Emissions Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load CSS
load_css()

# Load Data
df = load_data()
st.session_state.df = df

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.markdown("---")

    countries_list = sorted(df["country"].dropna().unique().tolist())

    if "selected_country" not in st.session_state:
        st.session_state.selected_country = "Philippines" if "Philippines" in countries_list else countries_list[0]

    st.session_state.selected_country = st.selectbox(
        "🔍 Primary Country",
        countries_list,
        index=countries_list.index(st.session_state.selected_country) if st.session_state.selected_country in countries_list else 0,
    )

    all_years = df["year"].dropna().unique()
    min_yr, max_yr = int(all_years.min()), int(all_years.max())
    
    if "year_range" not in st.session_state:
        st.session_state.year_range = (1900, max_yr)

    st.session_state.year_range = st.slider("📅 Year Range", min_yr, max_yr, st.session_state.year_range)

    st.markdown("---")
    
    default_compare = ["United States", "China", "India"]
    valid_default = [c for c in default_compare if c in countries_list and c != st.session_state.selected_country]

    if "compare_countries" not in st.session_state:
        st.session_state.compare_countries = valid_default

    st.session_state.compare_countries = st.multiselect(
        "📊 Compare Countries",
        [c for c in countries_list if c != st.session_state.selected_country],
        default=[c for c in st.session_state.compare_countries if c != st.session_state.selected_country],
        max_selections=6,
    )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#555; font-size:0.75rem; margin-top:1rem;'>"
        "Data: Our World in Data<br>Built with Streamlit + Plotly</div>",
        unsafe_allow_html=True,
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER & KPIs (Global for all pages)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
render_header()
has_data, country_df, country_co2 = render_kpi_metrics(
    df, st.session_state.selected_country, st.session_state.year_range
)

if has_data:
    st.session_state.country_df = country_df
    st.session_state.country_co2 = country_co2

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PAGING & NAVIGATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    pg = st.navigation([
        st.Page("views/1_Overview.py", title="Overview", icon="📈"),
        st.Page("views/2_Emission_Sources.py", title="Emission Sources", icon="⛽"),
        st.Page("views/3_Country_Comparison.py", title="Country Comparison", icon="🔀"),
        st.Page("views/4_Global_Map.py", title="Global Map", icon="🗺️"),
        st.Page("views/5_Predictions.py", title="Predictions", icon="🔮"),
        st.Page("views/6_Deep_Analytics.py", title="Deep Analytics", icon="🧪"),
        st.Page("views/7_Data_Explorer.py", title="Data Explorer", icon="📋"),
    ])
    pg.run()
