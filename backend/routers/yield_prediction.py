import pandas as pd
from fastapi import APIRouter
from backend.schemas import YieldInput, YieldOutput
from backend.utils.model_loader import yield_model, yield_preprocessor

router = APIRouter()


@router.post("/predict-yield", response_model=YieldOutput)
def predict_yield(data: YieldInput):
    # Derived / engineered features (must match training exactly)
    rain_temp_ratio = data.average_rain_fall_mm_per_year / (data.avg_temp + 1)
    pesticide_per_rain = data.pesticides_tonnes / (data.average_rain_fall_mm_per_year + 1)
    decade = (data.Year // 10) * 10

    # Build a single-row DataFrame — preprocessor expects named columns, not a raw array
    input_df = pd.DataFrame([{
        "Area": data.Area,
        "Item": data.Item,
        "Year": data.Year,
        "average_rain_fall_mm_per_year": data.average_rain_fall_mm_per_year,
        "pesticides_tonnes": data.pesticides_tonnes,
        "avg_temp": data.avg_temp,
        "rain_temp_ratio": rain_temp_ratio,
        "pesticide_per_rain": pesticide_per_rain,
        "decade": decade,
    }])

    # Preprocessor handles both StandardScaler (numeric) + OneHotEncoder (Area, Item)
    transformed = yield_preprocessor.transform(input_df)

    prediction_hg_per_ha = float(yield_model.predict(transformed)[0])
    prediction_tonnes_per_ha = prediction_hg_per_ha / 10000

    return YieldOutput(
        predicted_yield_hg_per_ha=round(prediction_hg_per_ha, 2),
        predicted_yield_tonnes_per_ha=round(prediction_tonnes_per_ha, 4),
    )