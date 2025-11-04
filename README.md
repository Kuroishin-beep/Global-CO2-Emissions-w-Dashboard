Global CO₂ Emissions Dashboard & Prediction

This project visualizes global CO₂ emissions data and predicts future emissions using Linear Regression.
It includes a React dashboard for visualization and a FastAPI backend for data processing and ML predictions.

Dataset used: https://www.kaggle.com/datasets/patricklford/global-co-emissions

Features

View historical CO₂ emission data by country

Predict future CO₂ emissions (2025–2050)

Interactive React dashboard

FastAPI backend with ML model

Country selector & real-time API updates

Technologies Used

Frontend: React, Axios, Chart.js

Backend: FastAPI, Pandas, NumPy, Scikit-Learn

ML Model: Linear Regression

Dataset: Kaggle CO₂ Global Dataset

Setup Instructions
Backend (FastAPI)
cd backend
pip install fastapi uvicorn pandas numpy scikit-learn
uvicorn main:app --reload


API runs at: http://127.0.0.1:8000

Frontend (React)
cd frontend
npm install
npm start


Runs at: http://localhost:3000

API Endpoints
Endpoint	Description
/countries	Get list of countries
/data/{country}	Get historical CO₂ data
/predict/{country}	Get predicted CO₂ values
/compare/{c1,c2}	Compare multiple countries
Notes

CSV path used in backend:
Data_Sets/global_co2_emissions.csv

Ensure backend is running before starting frontend

Predictions use simple Linear Regression for demonstration purposes

Future Improvements

Advanced forecasting models (ARIMA, LSTM)

Export charts and predictions

Live world map visualization

Deploy to cloud (Render / Vercel)
