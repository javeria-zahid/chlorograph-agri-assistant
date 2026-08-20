import numpy as np
from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
import tensorflow as tf

from backend.schemas import DiseaseOutput
from backend.utils.model_loader import disease_model, disease_class_names

router = APIRouter()


@router.post("/predict-disease", response_model=DiseaseOutput)
async def predict_disease(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))

    img_array = tf.keras.utils.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)
    # Note: no manual /255 rescaling needed — preprocess_input is baked into the model itself

    predictions = disease_model.predict(img_array)
    predicted_index = int(np.argmax(predictions[0]))
    confidence = float(np.max(tf.nn.softmax(predictions[0])))

    disease_name = disease_class_names[predicted_index]

    return DiseaseOutput(disease=disease_name, confidence=round(confidence, 4))