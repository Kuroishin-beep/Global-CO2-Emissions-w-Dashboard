import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#A5A8BD"),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor="rgba(108,99,255,0.07)", zerolinecolor="rgba(108,99,255,0.1)"),
    yaxis=dict(gridcolor="rgba(108,99,255,0.07)", zerolinecolor="rgba(108,99,255,0.1)"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
    hoverlabel=dict(bgcolor="#1E2235", font_size=13, font_family="Inter"),
)

COLORS = ["#6C63FF", "#06B6D4", "#F59E0B", "#EF4444", "#10B981", "#EC4899", "#8B5CF6", "#F97316"]

def apply_layout(fig, title="", height=420):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=15, color="#FAFAFA")), height=height)
    return fig

def classify_emitter(max_co2):
    if max_co2 < 50:
        return "🟢 Low Emitter", "#10B981", "Very low CO₂ output — likely small population or heavy renewable use."
    elif max_co2 < 300:
        return "🟡 Moderate Emitter", "#F59E0B", "Moderate emissions from growing industry and urbanization."
    elif max_co2 < 1000:
        return "🟠 High Emitter", "#F97316", "Significant emissions driven by industrialization and energy demand."
    else:
        return "🔴 Very High Emitter", "#EF4444", "Among the world's largest CO₂ emitters — heavy fossil fuel reliance."

def predict_emissions(country_df, future_years=None):
    if future_years is None:
        future_years = list(range(2025, 2056, 5))
    data = country_df[["year", "co2"]].dropna()
    if len(data) < 3:
        return pd.DataFrame()
    X = data["year"].values.reshape(-1, 1)
    y = data["co2"].values
    model = LinearRegression().fit(X, y)
    future = np.array(future_years).reshape(-1, 1)
    preds = model.predict(future)
    r2 = model.score(X, y)
    return pd.DataFrame({
        "year": future_years,
        "predicted_co2": np.maximum(preds, 0),
        "r2_score": r2,
    })
