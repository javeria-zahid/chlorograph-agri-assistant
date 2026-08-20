from pydantic import BaseModel


# ---------- Crop Recommendation ----------
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class CropOutput(BaseModel):
    recommended_crop: str


# ---------- Fertilizer Recommendation ----------
class FertilizerInput(BaseModel):
    Soil_Type: str
    Soil_pH: float
    Soil_Moisture: float
    Organic_Carbon: float
    Electrical_Conductivity: float
    Nitrogen_Level: int
    Phosphorus_Level: int
    Potassium_Level: int
    Temperature: float
    Humidity: float
    Rainfall: float
    Crop_Type: str
    Crop_Growth_Stage: str
    Season: str
    Irrigation_Type: str
    Previous_Crop: str
    Region: str
    Fertilizer_Used_Last_Season: float
    Yield_Last_Season: float


class FertilizerOutput(BaseModel):
    recommended_fertilizer: str
    top_3_candidates: list[str]


# ---------- Crop Yield Prediction ----------
class YieldInput(BaseModel):
    Area: str
    Item: str
    Year: int
    average_rain_fall_mm_per_year: float
    pesticides_tonnes: float
    avg_temp: float


class YieldOutput(BaseModel):
    predicted_yield_hg_per_ha: float
    predicted_yield_tonnes_per_ha: float


# ---------- Disease Prediction ----------
class DiseaseOutput(BaseModel):
    disease: str
    confidence: float