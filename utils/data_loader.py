import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data_Sets", "global_co2_emissions.csv")
    df = pd.read_csv(csv_path)
    # Ensure numeric types
    for col in ["co2", "co2_per_capita", "population", "gdp", "coal_co2", "oil_co2", "gas_co2", "cement_co2",
                "co2_growth_prct", "cumulative_co2", "methane", "nitrous_oxide", "total_ghg",
                "share_global_co2", "co2_per_gdp", "primary_energy_consumption",
                "temperature_change_from_co2", "temperature_change_from_ghg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df
