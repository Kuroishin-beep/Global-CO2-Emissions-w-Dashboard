import streamlit as st

country_df = st.session_state.country_df
selected_country = st.session_state.selected_country

st.markdown('<div class="section-title"><span class="icon">📋</span> Raw Data Explorer</div>', unsafe_allow_html=True)

# Column selector
available_cols = [c for c in country_df.columns if country_df[c].notna().any()]
default_cols = ["year", "co2", "co2_per_capita", "population", "gdp", "coal_co2", "oil_co2", "gas_co2"]
default_cols = [c for c in default_cols if c in available_cols]

selected_cols = st.multiselect("Select columns", available_cols, default=default_cols)

if selected_cols:
    display_df = country_df[selected_cols].dropna(how="all").reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, height=500)

    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, f"{selected_country}_co2_data.csv", "text/csv")
    with col2:
        st.metric("Rows", f"{len(display_df):,}")
    with col3:
        st.metric("Columns", len(selected_cols))
else:
    st.info("Select at least one column to view data.")
