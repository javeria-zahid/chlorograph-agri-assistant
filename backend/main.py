from fastapi import FastAPI
from backend.routers import crop, fertilizer, yield_prediction, disease

app = FastAPI(
    title="AI Agriculture Assistant",
    description="Unified API for crop recommendation, fertilizer recommendation, "
                 "crop yield prediction, and plant disease prediction.",
    version="1.0.0",
)

app.include_router(crop.router, tags=["Crop Recommendation"])
app.include_router(fertilizer.router, tags=["Fertilizer Recommendation"])
app.include_router(yield_prediction.router, tags=["Crop Yield Prediction"])
app.include_router(disease.router, tags=["Disease Prediction"])


@app.get("/")
def root():
    return {"message": "AI Agriculture Assistant API is running. Visit /docs to test all endpoints."}