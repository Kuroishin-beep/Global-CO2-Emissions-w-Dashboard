import os
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests

app = FastAPI()

class InsightRequest(BaseModel):
    country: str
    year: int
    co2: float

# Free models to try in order. If one is rate-limited (429), fall back to the next.
FALLBACK_MODELS = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "qwen/qwen-2.5-7b-instruct:free",
]

MAX_RETRIES_PER_MODEL = 2
BASE_BACKOFF_SECONDS = 1.5


def call_openrouter(api_key: str, prompt: str):
    """
    Try each model in FALLBACK_MODELS in order. For each model, retry on 429
    with exponential backoff before moving to the next model.
    Returns the parsed JSON response on success, raises the last error otherwise.
    """
    last_error = None

    for model in FALLBACK_MODELS:
        for attempt in range(MAX_RETRIES_PER_MODEL):
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
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are an expert environmental data analyst. Provide a brief, professional insight based on the provided CO2 data (1-3 sentences maximum)."},
                            {"role": "user", "content": prompt}
                        ]
                    }
                )

                if response.status_code == 429:
                    last_error = response
                    wait = BASE_BACKOFF_SECONDS * (2 ** attempt)
                    print(f"[OpenRouter] 429 on {model} (attempt {attempt + 1}), backing off {wait}s")
                    time.sleep(wait)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                last_error = "timeout"
                print(f"[OpenRouter] Timeout on {model} (attempt {attempt + 1})")
                continue
            except requests.exceptions.HTTPError as e:
                # Non-429 HTTP error: don't bother retrying this model, try the next one.
                last_error = e
                print(f"[OpenRouter] HTTP error on {model}: {e.response.text if e.response else e}")
                break

        # exhausted retries for this model (or non-retryable error) -> try next model

    # All models/retries exhausted
    if last_error == "timeout":
        raise requests.exceptions.Timeout()
    if isinstance(last_error, requests.exceptions.HTTPError):
        raise last_error
    if last_error is not None and getattr(last_error, "status_code", None) == 429:
        raise HTTPException(status_code=429, detail="All free models are currently rate-limited. Please try again shortly.")
    raise HTTPException(status_code=500, detail="Unable to reach AI service.")


@app.get("/api/health")
def health():
    key = os.environ.get("OPENROUTER_API_KEY")
    return {
        "key_present": key is not None,
        "key_prefix": key[:8] + "..." if key else None
    }

print("DEPLOY_MARKER_v2")
@app.post("/api/insights")
def get_insights(req: InsightRequest):
    prompt = f"Analyze CO2 for {req.country}. In {req.year}, it was {req.co2} Mt."
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="API key is missing.")
        
    try:
        result = call_openrouter(api_key, prompt)
        insight = result.get("choices", [{}])[0].get("message", {}).get("content", "Error generating insight.")
        return {"insight": insight}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request to AI service timed out.")
    except requests.exceptions.HTTPError as e:
        error_details = e.response.text if e.response else str(e)
        print(f"OpenRouter API Error: {error_details}")
        status = e.response.status_code if e.response else 500
        raise HTTPException(status_code=500, detail=f"Upstream AI Error ({status})")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching insight: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while generating insights.")