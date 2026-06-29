import os
import json
from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

app = FastAPI()

class InsightRequest(BaseModel):
    country: str
    year: int
    co2: float

@app.get("/api/data")
def get_data():
    # Read the data from public/data.json
    try:
        with open(os.path.join("public", "data.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Data not available")

@app.post("/api/insights")
def get_insights(req: InsightRequest):
    prompt = f"Analyze CO2 for {req.country}. In {req.year}, it was {req.co2} Mt."
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        import time
        time.sleep(1.5)
        text = f"{req.country} make much fire in {req.year}. {req.co2} big smoke. Earth get hot. Must stop fire. Use sun. Use wind."
        if req.co2 < 50:
            text = f"{req.country} make small fire. Only {req.co2} smoke. Good. Keep air clean."
        return {"insight": text}
        
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}", 
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5173", # Optional but recommended by OpenRouter
                "X-Title": "Global CO2 Dashboard"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct:free", # Free model available on OpenRouter
                "messages": [
                    {"role": "system", "content": "You are a caveman. Speak short and efficiently."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        result = response.json()
        insight = result.get("choices", [{}])[0].get("message", {}).get("content", "Error make thought.")
        return {"insight": insight}
    except Exception as e:
        print(f"Error fetching insight: {e}")
        raise HTTPException(status_code=500, detail="Brain hurt. No think now.")
