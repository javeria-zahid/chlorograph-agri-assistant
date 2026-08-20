import streamlit as st
import requests
from components import load_css, page_header, result_card, empty_state, API_BASE_URL

st.set_page_config(page_title="Disease Detection · AgriAssist", page_icon="🍃", layout="wide")
load_css()

page_header(
    eyebrow="Module 04 · EfficientNetB0 · 98.4% Val. Accuracy",
    title="What's wrong with this leaf?",
    subtitle="Upload a photo of a leaf — a fine-tuned EfficientNetB0 model classifies it across 38 disease/health states spanning 14 crops.",
    accent_word="this leaf?",
)

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-title">Upload a leaf photo</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Clear, well-lit, single-leaf photos work best.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Leaf image", type=["jpg", "jpeg", "png", "jfif", "webp", "bmp"], label_visibility="collapsed")

    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

    submit = st.button("Detect disease", use_container_width=True, disabled=uploaded_file is None)

with right:
    st.markdown('<div class="section-title">Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">&nbsp;</div>', unsafe_allow_html=True)

    if submit and uploaded_file:
        try:
            with st.spinner("Running inference across 38 classes..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                res = requests.post(f"{API_BASE_URL}/predict-disease", files=files, timeout=30)
                res.raise_for_status()
                data = res.json()

            disease_raw = data["disease"]
            is_healthy = "healthy" in disease_raw.lower()
            crop, condition = (disease_raw.split("___") + [""])[:2]
            display_value = "Healthy ✓" if is_healthy else condition.replace("_", " ")

            result_card(
                label=f"{crop.replace('_', ' ')} — Diagnosis",
                value=display_value,
                tone="success" if is_healthy else "warning",
                confidence=data.get("confidence"),
                note=None if is_healthy else "Consider isolating affected plants and consulting a local agronomist for treatment options.",
            )
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Make sure `uvicorn backend.main:app --reload` is running.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        empty_state("🍃", "Upload a leaf photo and click Detect disease to see a diagnosis here.")