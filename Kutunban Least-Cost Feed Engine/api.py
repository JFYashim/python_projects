import json
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from engine.solver import FeedOptimizer

app = FastAPI(
    title="Kutunban Least-Cost Feed API",
    description="Backend optimization engine for Kaduna livestock farmers",
    version="1.0.0"
)

# File paths setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INGREDIENTS_PATH = os.path.join(BASE_DIR, "data", "ingredients.json")
PROFILES_PATH = os.path.join(BASE_DIR, "data", "profiles.json")

def load_data():
    with open(INGREDIENTS_PATH, "r") as f:
        ingredients = json.load(f)
    with open(PROFILES_PATH, "r") as f:
        profiles = json.load(f)
    return ingredients, profiles

class OptimizeRequest(BaseModel):
    profile_key: str
    batch_size_kg: float = 100.0
    custom_ingredients: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root():
    return {"status": "online", "system": "Kutunban LCF Engine API"}

@app.get("/profiles")
def get_profiles():
    _, profiles = load_data()
    return profiles

@app.get("/ingredients")
def get_ingredients():
    ingredients, _ = load_data()
    return ingredients

@app.post("/optimize")
def optimize_feed(req: OptimizeRequest):
    ingredients, profiles = load_data()
    
    if req.profile_key not in profiles:
        raise HTTPException(status_code=400, detail=f"Profile '{req.profile_key}' not found.")

    # Override with custom prices if provided by the mobile app
    if req.custom_ingredients:
        ingredients.update(req.custom_ingredients)

    target_profile = profiles[req.profile_key]
    optimizer = FeedOptimizer(ingredients)
    
    recipe, total_cost, status = optimizer.solve(target_profile, batch_size_kg=req.batch_size_kg)

    if status != "Optimal":
        raise HTTPException(status_code=422, detail=f"Optimization failed: {status}")

    return {
        "status": status,
        "profile_name": target_profile["name"],
        "batch_size_kg": req.batch_size_kg,
        "total_cost_ngn": total_cost,
        "cost_per_kg_ngn": round(total_cost / req.batch_size_kg, 2),
        "cost_per_25kg_bag_ngn": round((total_cost / req.batch_size_kg) * 25, 2),
        "recipe_kg": recipe
    }
