# 🌿 Chlorograph — AI Agriculture Assistant

> An end-to-end precision agriculture system that recommends what to plant, what to feed it, forecasts what it will yield, and diagnoses leaf disease from a photo — four independently trained ML models, unified behind a single FastAPI backend with a custom-designed Streamlit dashboard.


##video : https://drive.google.com/file/d/1qbNeUGTk5XVTbtqJ3HoxYIvz4Y5LLzH5/view?usp=sharing--

## Table of Contents

- [Overview](#overview)
- [Modules](#modules)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Model Details](#model-details)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

Chlorograph combines four separately trained machine learning models into one decision-support system for farmers and agronomists:

1. Decide **what crop** to plant based on soil and climate
2. Decide **what to feed** that crop
3. Estimate **what it will yield**
4. Diagnose **what's wrong** with it from a leaf photo

Each module was trained independently (different datasets, different model families — Random Forest, XGBoost, and a fine-tuned CNN), then integrated behind one FastAPI backend so the whole system can be operated through a single dashboard.

This was built as a final-year capstone / internship project, covering the full ML lifecycle: data preprocessing → model training & evaluation → backend API design → frontend integration → deployment.

## Modules

| # | Module | Model | Input | Output |
|---|---|---|---|---|
| 01 | 🌾 Crop Recommendation | Random Forest Classifier | N, P, K, temperature, humidity, pH, rainfall | Best-fit crop (22 classes) |
| 02 | 🧪 Fertilizer Recommendation | XGBoost Classifier | 19 features — soil chemistry, crop stage, season history | Recommended fertilizer + top-3 alternatives (7 classes) |
| 03 | 📈 Crop Yield Prediction | Random Forest Regressor | Area, crop, year, rainfall, pesticide use, avg. temperature | Predicted yield (hg/ha and tonnes/ha) |
| 04 | 🍃 Disease Detection | EfficientNetB0 (transfer learning) | Leaf photo (JPG/PNG) | Disease diagnosis across 38 classes, 14 crops + confidence score |

## Tech Stack

**Machine Learning**
- scikit-learn (Random Forest — crop, yield)
- XGBoost (fertilizer)
- TensorFlow / Keras — EfficientNetB0 transfer learning (disease)
- Trained on Google Colab (T4 GPU)

**Backend**
- FastAPI + Uvicorn
- Pydantic schemas for request/response validation
- joblib (scikit-learn/XGBoost model persistence)

**Frontend**
- Streamlit, with a fully custom CSS theme (no default Streamlit styling)
- Custom typography (Space Grotesk / Inter / IBM Plex Mono), dark "field-sensor" visual theme, animated UI

**Data**
- Crop recommendation: soil N-P-K + climate dataset
- Fertilizer recommendation: soil chemistry + crop context dataset
- Yield prediction: FAO / World Bank agricultural yield data
- Disease detection: [PlantVillage dataset](https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset) (54,305 images, 38 classes, 14 crops)

## System Architecture

```
┌─────────────────────┐         HTTP/JSON          ┌──────────────────────┐
│  Streamlit Dashboard │ ─────────────────────────▶ │   FastAPI Backend     │
│  (dashboard/)        │ ◀───────────────────────── │   (backend/)          │
└─────────────────────┘                             └──────────┬───────────┘
                                                                │
                                                     ┌──────────▼───────────┐
                                                     │   models/             │
                                                     │  ├── crop/            │
                                                     │  ├── fertilizer/      │
                                                     │  ├── yield/           │
                                                     │  └── disease/         │
                                                     └───────────────────────┘
```

The dashboard never touches the models directly — every prediction goes through the FastAPI backend's REST endpoints. This keeps the frontend and ML logic fully decoupled, so either can be redeployed or swapped independently.

## Project Structure

```
AI-Agriculture-Assistant/
│
├── backend/
│   ├── main.py                    # FastAPI app entrypoint, mounts all routers
│   ├── schemas.py                 # Pydantic request/response models
│   ├── routers/
│   │   ├── crop.py                # POST /predict-crop
│   │   ├── fertilizer.py          # POST /predict-fertilizer
│   │   ├── yield_prediction.py    # POST /predict-yield
│   │   └── disease.py             # POST /predict-disease
│   └── utils/
│       └── model_loader.py        # Loads all models + encoders once at startup
│
├── dashboard/
│   ├── app.py                     # Landing page — module selector
│   ├── components.py              # Shared styled UI components
│   ├── assets/
│   │   └── style.css              # Custom theme (colors, fonts, animations)
│   └── pages/
│       ├── 1_Crop_Recommendation.py
│       ├── 2_Fertilizer_Recommendation.py
│       ├── 3_Crop_Yield_Prediction.py
│       └── 4_Disease_Prediction.py
│
├── models/
│   ├── crop/                      # crop_recommendation_model.pkl, label_encoder.pkl
│   ├── fertilizer/                # fertilizer_recommendation_model.json + 8 encoders + scaler
│   ├── yield/                     # crop_yield_model.pkl, preprocessor.pkl
│   └── disease/                   # disease_prediction_model.keras
│
├── notebooks/                     # Original Colab training notebooks
├── data/                          # Reference/training datasets
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.10+
- pip

### 1. Clone and set up the environment

```bash
git clone https://github.com/YOUR_USERNAME/chlorograph-agri-assistant.git
cd chlorograph-agri-assistant

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2. Start the backend

```bash
uvicorn backend.main:app --reload
```

Backend runs at `http://127.0.0.1:8000` — interactive API docs at `http://127.0.0.1:8000/docs`.

### 3. Start the dashboard (in a second terminal)

```bash
streamlit run dashboard/app.py
```

Dashboard opens at `http://localhost:8501`.

> Both must be running simultaneously — the dashboard calls the backend over HTTP for every prediction.

## API Reference

All endpoints accept/return JSON (disease detection accepts `multipart/form-data` for the image file).

| Endpoint | Method | Description |
|---|---|---|
| `/predict-crop` | POST | Returns recommended crop from soil/climate inputs |
| `/predict-fertilizer` | POST | Returns recommended fertilizer + top-3 candidates |
| `/predict-yield` | POST | Returns predicted yield in hg/ha and tonnes/ha |
| `/predict-disease` | POST | Accepts an image file, returns disease class + confidence |

Full request/response schemas are auto-documented at `/docs` (Swagger UI) once the backend is running.

## Model Details

**Disease Detection (the deep learning module)**
- Base: EfficientNetB0, ImageNet-pretrained
- Training strategy: two-phase — frozen-base head training, then fine-tuning the top 30 layers at a low learning rate
- Dataset: PlantVillage, 38 classes, 43,444 train / 10,861 validation images
- **Final validation accuracy: 98.4%**, validation loss 0.053, no signs of overfitting

**Crop / Fertilizer / Yield (tabular ML modules)**
- Crop: RandomForestClassifier, 7 input features, 22 crop classes
- Fertilizer: XGBoost, 19 input features (8 label-encoded categoricals + scaler), 7 fertilizer classes
- Yield: RandomForestRegressor with a `ColumnTransformer` preprocessing pipeline (StandardScaler + OneHotEncoder), engineered features (rain/temp ratio, pesticide/rain ratio, decade)


## Roadmap

- [ ] Add authentication for multi-user usage tracking
- [ ] Cache repeated predictions
- [ ] Add explainability (SHAP) for the tabular models
- [ ] Expand disease dataset with region-specific crops

## Author

Built by **Javeria Zahid** — Final-year Computer Software Engineer

