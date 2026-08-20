"""
Loads all trained models and their preprocessing artifacts once at startup.
Import from this module in your routers instead of loading files per-request.
"""

import joblib
import tensorflow as tf

# ---------- Crop Recommendation ----------
crop_model = joblib.load("models/crop/crop_recommendation_model.pkl")
crop_label_encoder = joblib.load("models/crop/label_encoder.pkl")

# ---------- Fertilizer Recommendation ----------
from xgboost import XGBClassifier

fertilizer_model = XGBClassifier()
fertilizer_model.load_model("models/fertilizer/fertilizer_recommendation_model.json")

fertilizer_encoders = {
    "soil": joblib.load("models/fertilizer/le_soil.pkl"),
    "crop": joblib.load("models/fertilizer/le_crop.pkl"),
    "growth_stage": joblib.load("models/fertilizer/le_growth_stage.pkl"),
    "season": joblib.load("models/fertilizer/le_season.pkl"),
    "irrigation": joblib.load("models/fertilizer/le_irrigation.pkl"),
    "previous_crop": joblib.load("models/fertilizer/le_previous_crop.pkl"),
    "region": joblib.load("models/fertilizer/le_region.pkl"),
    "fert": joblib.load("models/fertilizer/le_fert.pkl"),  # target decoder only
}
fertilizer_scaler = joblib.load("models/fertilizer/scaler.pkl")

# ---------- Crop Yield Prediction ----------
yield_model = joblib.load("models/yield/crop_yield_model.pkl")
yield_preprocessor = joblib.load("models/yield/preprocessor.pkl")

# ---------- Disease Prediction ----------
disease_model = tf.keras.models.load_model("models/disease/disease_prediction_model.keras")

disease_class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
]

print("All models loaded successfully.")