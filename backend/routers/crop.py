import numpy as np
from fastapi import APIRouter
from backend.schemas import CropInput, CropOutput
from backend.utils.model_loader import crop_model, crop_label_encoder

router = APIRouter()


@router.post("/predict-crop", response_model=CropOutput)
def predict_crop(data: CropInput):
    features = np.array([[
        data.N, data.P, data.K,
        data.temperature, data.humidity,
        data.ph, data.rainfall
    ]])

    prediction = crop_model.predict(features)
    crop_name = crop_label_encoder.inverse_transform(prediction)[0]

    return CropOutput(recommended_crop=crop_name)