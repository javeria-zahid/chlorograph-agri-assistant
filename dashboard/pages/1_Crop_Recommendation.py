import streamlit as st
import requests
from components import load_css, page_header, result_card, empty_state, API_BASE_URL

st.set_page_config(page_title="Crop Recommendation · AgriAssist", page_icon="🌾", layout="wide")
load_css()

page_header(
    eyebrow="Module 01 · Random Forest Classifier",
    title="What should you plant?",
    subtitle="Enter your soil's nutrient profile and local climate readings — the model matches them against 22 crop classes.",
    accent_word="plant?",
)

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Field readings</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All values as measured on-site or from your last soil test.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    N = c1.number_input("Nitrogen (N)", 0, 200, 90)
    P = c2.number_input("Phosphorus (P)", 0, 200, 42)
    K = c3.number_input("Potassium (K)", 0, 200, 43)

    c4, c5 = st.columns(2)
    temperature = c4.number_input("Temperature (°C)", -10.0, 55.0, 25.0)
    humidity = c5.number_input("Humidity (%)", 0.0, 100.0, 71.0)

    c6, c7 = st.columns(2)
    ph = c6.number_input("Soil pH", 0.0, 14.0, 6.5)
    rainfall = c7.number_input("Rainfall (mm)", 0.0, 3000.0, 200.0)

    submit = st.button("Recommend crop", use_container_width=True)

with right:
    st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">&nbsp;</div>', unsafe_allow_html=True)

    if submit:
        payload = {
            "N": N, "P": P, "K": K,
            "temperature": temperature, "humidity": humidity,
            "ph": ph, "rainfall": rainfall,
        }
        try:
            with st.spinner("Matching field profile against 22 crop classes..."):
                res = requests.post(f"{API_BASE_URL}/predict-crop", json=payload, timeout=15)
                res.raise_for_status()
                data = res.json()
            result_card(
                label="Recommended Crop",
                value=data["recommended_crop"].title(),
                tone="success",
                note="Based on your N-P-K balance, climate, and soil pH.",
            )
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Make sure `uvicorn backend.main:app --reload` is running.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        empty_state("🌾", "Fill in the field readings and click Recommend crop to see a result here.")