import streamlit as st
import requests
from components import load_css, page_header, result_card, empty_state, API_BASE_URL

st.set_page_config(page_title="Yield Prediction · AgriAssist", page_icon="📈", layout="wide")
load_css()

page_header(
    eyebrow="Module 03 · Random Forest Regressor",
    title="What will your field actually produce?",
    subtitle="Forecasts yield from historical climate and input-use patterns, trained on FAO / World Bank agricultural data.",
    accent_word="actually produce?",
)

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Region &amp; season inputs</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    area = c1.text_input("Country / Area", "Pakistan")
    item = c2.text_input("Crop item", "Wheat")

    c3, c4 = st.columns(2)
    year = c3.number_input("Year", 1960, 2035, 2024)
    avg_temp = c4.number_input("Average temperature (°C)", -10.0, 55.0, 20.0)

    c5, c6 = st.columns(2)
    rainfall = c5.number_input("Average rainfall (mm/year)", 0.0, 5000.0, 1000.0)
    pesticides = c6.number_input("Pesticides used (tonnes)", 0.0, 5000.0, 100.0)

    submit = st.button("Predict yield", use_container_width=True)

with right:
    st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">&nbsp;</div>', unsafe_allow_html=True)

    if submit:
        payload = {
            "Area": area,
            "Item": item,
            "Year": year,
            "average_rain_fall_mm_per_year": rainfall,
            "pesticides_tonnes": pesticides,
            "avg_temp": avg_temp,
        }
        try:
            with st.spinner("Running regression model..."):
                res = requests.post(f"{API_BASE_URL}/predict-yield", json=payload, timeout=15)
                res.raise_for_status()
                data = res.json()
            result_card(
                label="Predicted Yield",
                value=f"{data['predicted_yield_tonnes_per_ha']} t/ha",
                tone="success",
                note=f"Raw model output: {data['predicted_yield_hg_per_ha']:,} hg/ha",
            )
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Make sure `uvicorn backend.main:app --reload` is running.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        empty_state("📈", "Fill in the region and climate inputs, then click Predict yield.")