import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

app = FastAPI()

class InsightRequest(BaseModel):
    country: str
    year: int
    co2: float


@app.get("/api/health")
def health():
    key = os.environ.get("OPENROUTER_API_KEY")
    return {
        "key_present": key is not None,
        "key_prefix": key[:8] + "..." if key else None
    }


@app.post("/api/insights")
def get_insights(req: InsightRequest):
    prompt = f"Analyze CO2 for {req.country}. In {req.year}, it was {req.co2} Mt."
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is missing.")
        
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            timeout=8,
            headers={
                "Authorization": f"Bearer {api_key}", 
                "Content-Type": "application/json",
                "HTTP-Referer": "https://global-co-2-emissions-w-das-git-a54a9f-kuroishin-beeps-projects.vercel.app/overview",
                "X-Title": "Global CO2 Dashboard"
            },
            json={
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are an expert environmental data analyst. Provide a brief, professional insight based on the provided CO2 data (1-3 sentences maximum)."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        
        response.raise_for_status() 
        
        result = response.json()
        insight = result.get("choices", [{}])[0].get("message", {}).get("content", "Error generating insight.")
        return {"insight": insight}
        
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to AI service timed out.")
    except requests.exceptions.HTTPError as e:
        error_details = e.response.text if e.response else str(e)
        print(f"OpenRouter API Error: {error_details}")
        status = e.response.status_code if e.response else 500
        raise HTTPException(status_code=500, detail=f"Upstream AI Error ({status})")
    except Exception as e:
        print(f"Error fetching insight: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while generating insights.")