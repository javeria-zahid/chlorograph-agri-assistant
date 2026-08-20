import joblib

encoders = {
    "Soil_Type": "models/fertilizer/le_soil.pkl",
    "Crop_Type": "models/fertilizer/le_crop.pkl",
    "Crop_Growth_Stage": "models/fertilizer/le_growth_stage.pkl",
    "Season": "models/fertilizer/le_season.pkl",
    "Irrigation_Type": "models/fertilizer/le_irrigation.pkl",
    "Previous_Crop": "models/fertilizer/le_previous_crop.pkl",
    "Region": "models/fertilizer/le_region.pkl",
    "Recommended_Fertilizer (target)": "models/fertilizer/le_fert.pkl",
}

for field, path in encoders.items():
    le = joblib.load(path)
    print(f"\n{field}:")
    print(list(le.classes_))