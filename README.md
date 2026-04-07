# 🌍 Global CO₂ Emissions Dashboard & Prediction

A simple data analytics project that visualizes **global CO₂ emissions** and predicts future values using **Linear Regression**.

Dataset Source:  
https://www.kaggle.com/datasets/patricklford/global-co-emissions

---

## 📌 Project Overview

This project consists of:

- **React Dashboard** for visualization  
- **FastAPI backend** for data access & ML predictions  
- **Linear Regression model** using scikit-learn  
- Country-based CO₂ data filtering and future prediction (2025–2050)

---

## Features

- Historical CO₂ emission plots per country  
- Future emission prediction (2025-2050)  
- Country selector dropdown  
- Live charts fetched from FastAPI  
- Kaggle dataset integration  

---

## Tech Stack

| Category | Tools / Technologies |
|---------|----------------------|
| **Frontend**          | ![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB) ![Axios](https://img.shields.io/badge/Axios-5A29E4?logo=axios&logoColor=white) ![Chart.js](https://img.shields.io/badge/Chart.js-F5788D?logo=chart.js&logoColor=white) |
| **Backend**           | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) |
| **Libraries**         | ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?logo=scikit-learn&logoColor=white)  |
| **Machine Learning**  | Linear Regression |
| **Dataset**           | Global CO₂ Emissions — Kaggle |


---

## Installation

### Backend (FastAPI)

```bash
cd backend
pip install fastapi uvicorn pandas numpy scikit-learn
uvicorn main:app --reload
````

---


## 📡 API Endpoints

| Route                  | Description                  |
| ---------------------- | ---------------------------- |
| `/countries`           | Get all countries            |
| `/data/{country}`      | Historical CO₂ data          |
| `/predict/{country}`   | Linear regression prediction |
| `/compare/{c1,c2,...}` | Compare multiple countries   |

---

## 📁 CSV Path

```
Data_Sets/global_co2_emissions.csv
```

---

## Future Improvements

* Better forecasting (ARIMA / LSTM models)
* Global heatmap visualization
* Deployment to Vercel + Render
* Add database caching

---


### Notes

* Ensure backend runs before starting the frontend
* Predictions are for demonstration (linear regression only)

---

### Goal

To demonstrate **data visualization + machine learning + full-stack integration** using real-world environmental data.

```
=======
# 🌍 Global CO₂ Emissions Dashboard

An interactive data analytics dashboard built with **Streamlit** and **Plotly** for exploring worldwide carbon dioxide emissions — historical trends, forecasts, and deep analytics.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-3F4F75?logo=plotly&logoColor=white)

## ✨ Features

| Feature | Description |
|---------|-------------|
| **📈 Overview** | Historical CO₂ charts (line, area, bar, scatter) with YoY growth rates |
| **⛽ Emission Sources** | Breakdown by coal, oil, gas, and cement with stacked area + pie charts |
| **🔀 Country Comparison** | Side-by-side comparison of up to 6 countries (total + per capita) |
| **🗺️ Global Map** | Interactive choropleth map by total CO₂, per capita, or global share |
| **🔮 Predictions** | Linear regression forecasting to 2050 with confidence bands |
| **🧪 Deep Analytics** | CO₂ vs GDP/population correlations, GHG composition, temperature contribution |
| **📋 Data Explorer** | Browse, filter, and download raw data as CSV |

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/your-username/Global-CO2-Emissions-w-Dashboard.git
cd Global-CO2-Emissions-w-Dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## 📁 Project Structure

```
├── app.py                  # Main Streamlit router & state manager
├── components/
│   └── metrics.py          # Render functions for global KPI indicators
├── utils/
│   ├── data_loader.py      # Data ingestion and caching
│   ├── helpers.py          # Formatting and math functions
│   └── style.py            # Custom CSS configurations
├── views/                  # Streamlit Multi-page application views
│   ├── 1_Overview.py
│   ├── 2_Emission_Sources.py
│   ├── 3_Country_Comparison.py
│   ├── 4_Global_Map.py
│   ├── 5_Predictions.py
│   ├── 6_Deep_Analytics.py
│   └── 7_Data_Explorer.py
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit theme & layout tweaks
├── Data_Sets/
│   └── global_co2_emissions.csv  # Source dataset
└── README.md
```

## 📊 Data Source

- [Our World in Data — CO₂ and Greenhouse Gas Emissions](https://github.com/owid/co2-data)

## 🛠️ Tech Stack

- **Streamlit** — Web framework
- **Plotly** — Interactive visualizations
- **Pandas / NumPy** — Data processing
- **Scikit-learn** — Linear regression forecasting
