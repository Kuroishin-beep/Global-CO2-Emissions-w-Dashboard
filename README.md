
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
