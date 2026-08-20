import numpy as np
from fastapi import APIRouter
from backend.schemas import FertilizerInput, FertilizerOutput
from backend.utils.model_loader import fertilizer_model, fertilizer_encoders, fertilizer_scaler

router = APIRouter()


@router.post("/predict-fertilizer", response_model=FertilizerOutput)
def predict_fertilizer(data: FertilizerInput):
    # Encode categorical fields with their respective encoders
    soil_encoded = fertilizer_encoders["soil"].transform([data.Soil_Type])[0]
    crop_encoded = fertilizer_encoders["crop"].transform([data.Crop_Type])[0]
    growth_stage_encoded = fertilizer_encoders["growth_stage"].transform([data.Crop_Growth_Stage])[0]
    season_encoded = fertilizer_encoders["season"].transform([data.Season])[0]
    irrigation_encoded = fertilizer_encoders["irrigation"].transform([data.Irrigation_Type])[0]
    previous_crop_encoded = fertilizer_encoders["previous_crop"].transform([data.Previous_Crop])[0]
    region_encoded = fertilizer_encoders["region"].transform([data.Region])[0]

    # Build the 19-feature array in EXACT training order
    features = np.array([[
        soil_encoded,
        data.Soil_pH,
        data.Soil_Moisture,
        data.Organic_Carbon,
        data.Electrical_Conductivity,
        data.Nitrogen_Level,
        data.Phosphorus_Level,
        data.Potassium_Level,
        data.Temperature,
        data.Humidity,
        data.Rainfall,
        crop_encoded,
        growth_stage_encoded,
        season_encoded,
        irrigation_encoded,
        previous_crop_encoded,
        region_encoded,
        data.Fertilizer_Used_Last_Season,
        data.Yield_Last_Season,
    ]])

    # Scale the entire 19-column array as one unit (encoded categoricals included)
    features_scaled = fertilizer_scaler.transform(features)

    # Get probabilities across all 7 fertilizer classes
    probabilities = fertilizer_model.predict_proba(features_scaled)[0]

    # Top prediction
    top_index = int(np.argmax(probabilities))
    recommended = fertilizer_encoders["fert"].inverse_transform([top_index])[0]

    # Top-3 candidates
    top_3_indices = np.argsort(probabilities)[::-1][:3]
    top_3_names = [
        fertilizer_encoders["fert"].inverse_transform([i])[0] for i in top_3_indices
    ]

    return FertilizerOutput(
        recommended_fertilizer=recommended,
        top_3_candidates=top_3_names,
    )