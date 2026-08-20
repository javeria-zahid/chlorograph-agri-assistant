import streamlit as st
import requests
from components import load_css, page_header, result_card, empty_state, API_BASE_URL

st.set_page_config(page_title="Fertilizer Recommendation · AgriAssist", page_icon="🧪", layout="wide")
load_css()

page_header(
    eyebrow="Module 02 · XGBoost Classifier",
    title="What should you feed the soil?",
    subtitle="19 features across soil chemistry, crop stage, and season history feed an XGBoost model trained on 7 fertilizer classes.",
    accent_word="feed the soil?",
)

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1.2, 1], gap="large")

SOIL_TYPES = ["Clay", "Loamy", "Sandy", "Silt"]
CROPS = ["Cotton", "Maize", "Potato", "Rice", "Sugarcane", "Tomato", "Wheat"]
GROWTH_STAGES = ["Flowering", "Harvest", "Sowing", "Vegetative"]
SEASONS = ["Kharif", "Rabi", "Zaid"]
IRRIGATION_TYPES = ["Canal", "Drip", "Rainfed", "Sprinkler"]
REGIONS = ["Central", "East", "North", "South", "West"]

with left:
    st.markdown('<div class="section-title">Soil &amp; crop profile</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Soil chemistry", "Crop context", "History"])

    with tab1:
        c1, c2 = st.columns(2)
        soil_type = c1.selectbox("Soil type", SOIL_TYPES)
        soil_ph = c2.number_input("Soil pH", 0.0, 14.0, 6.5)
        c3, c4 = st.columns(2)
        soil_moisture = c3.number_input("Soil moisture (%)", 0.0, 100.0, 35.0)
        organic_carbon = c4.number_input("Organic carbon (%)", 0.0, 10.0, 1.2)
        c5, c6 = st.columns(2)
        electrical_conductivity = c5.number_input("Electrical conductivity (dS/m)", 0.0, 20.0, 1.5)
        c7, c8, c9 = st.columns(3)
        nitrogen_level = c7.number_input("Nitrogen level", 0, 500, 80)
        phosphorus_level = c8.number_input("Phosphorus level", 0, 500, 40)
        potassium_level = c9.number_input("Potassium level", 0, 500, 40)

    with tab2:
        c1, c2 = st.columns(2)
        crop_type = c1.selectbox("Crop type", CROPS)
        crop_growth_stage = c2.selectbox("Growth stage", GROWTH_STAGES)
        c3, c4 = st.columns(2)
        season = c3.selectbox("Season", SEASONS)
        irrigation_type = c4.selectbox("Irrigation type", IRRIGATION_TYPES)
        c5, c6 = st.columns(2)
        temperature = c5.number_input("Temperature (°C)", -10.0, 55.0, 27.0)
        humidity = c6.number_input("Humidity (%)", 0.0, 100.0, 65.0)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 3000.0, 180.0)

    with tab3:
        c1, c2 = st.columns(2)
        previous_crop = c1.selectbox("Previous crop", CROPS)
        region = c2.selectbox("Region", REGIONS)
        c3, c4 = st.columns(2)
        fertilizer_last = c3.number_input("Fertilizer used last season (kg)", 0.0, 1000.0, 50.0)
        yield_last = c4.number_input("Yield last season (tonnes)", 0.0, 100.0, 4.5)

    submit = st.button("Recommend fertilizer", use_container_width=True)

with right:
    st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">&nbsp;</div>', unsafe_allow_html=True)

    if submit:
        payload = {
            "Soil_Type": soil_type,
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moisture,
            "Organic_Carbon": organic_carbon,
            "Electrical_Conductivity": electrical_conductivity,
            "Nitrogen_Level": nitrogen_level,
            "Phosphorus_Level": phosphorus_level,
            "Potassium_Level": potassium_level,
            "Temperature": temperature,
            "Humidity": humidity,
            "Rainfall": rainfall,
            "Crop_Type": crop_type,
            "Crop_Growth_Stage": crop_growth_stage,
            "Season": season,
            "Irrigation_Type": irrigation_type,
            "Previous_Crop": previous_crop,
            "Region": region,
            "Fertilizer_Used_Last_Season": fertilizer_last,
            "Yield_Last_Season": yield_last,
        }
        try:
            with st.spinner("Scoring against 7 fertilizer classes..."):
                res = requests.post(f"{API_BASE_URL}/predict-fertilizer", json=payload, timeout=15)
                res.raise_for_status()
                data = res.json()
            result_card(
                label="Recommended Fertilizer",
                value=data["recommended_fertilizer"],
                tone="success",
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-sub" style="margin-bottom:8px;">Other close candidates</div>', unsafe_allow_html=True)
            for i, cand in enumerate(data.get("top_3_candidates", [])[1:], start=2):
                st.markdown(
                    f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.85rem;'
                    f'color:var(--text-muted);padding:6px 0;border-bottom:1px solid var(--border);">'
                    f'#{i} — {cand}</div>',
                    unsafe_allow_html=True,
                )
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Make sure `uvicorn backend.main:app --reload` is running.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        empty_state("🧪", "Fill in the soil profile across all three tabs, then click Recommend fertilizer.")