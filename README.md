# 🌿 Chlorograph — AI Agriculture Assistant

An end-to-end precision agriculture system combining four independently trained ML models behind a single FastAPI backend, with a custom-designed Streamlit dashboard.

## Modules

| Module | Model | Task |
|---|---|---|
| 🌾 Crop Recommendation | Random Forest Classifier | Recommends the best crop from soil N-P-K, temperature, humidity, pH, rainfall |
| 🧪 Fertilizer Recommendation | XGBoost Classifier | Recommends optimal fertilizer from 19 soil/crop/environmental features |
| 📈 Crop Yield Prediction | Random Forest Regressor | Forecasts yield (hg/ha) from historical climate & pesticide-use data |
| 🍃 Disease Detection | EfficientNetB0 (Transfer Learning) | Classifies leaf photos across 38 disease/health states, 14 crops — 98.4% validation accuracy |

## Tech Stack

- **Backend:** FastAPI, scikit-learn, XGBoost, TensorFlow/Keras
- **Frontend:** Streamlit (custom CSS theme)
- **Training:** Google Colab (GPU), PlantVillage dataset

## Project Structure

```
├── backend/           # FastAPI app
│   ├── main.py
│   ├── schemas.py
│   ├── routers/       # One router per module
│   └── utils/         # Model loading
├── dashboard/          # Streamlit app
│   ├── app.py
│   ├── components.py
│   ├── assets/style.css
│   └── pages/          # One page per module
├── models/             # Trained model files, organized by module
└── notebooks/          # Training notebooks
```

## Running Locally

```bash
# 1. Set up environment
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# 2. Start the backend (Terminal 1)
uvicorn backend.main:app --reload

# 3. Start the dashboard (Terminal 2)
streamlit run dashboard/app.py
```

The dashboard runs at `http://localhost:8501`, backend API docs at `http://localhost:8000/docs`.

## Author

Javeria Zahid
