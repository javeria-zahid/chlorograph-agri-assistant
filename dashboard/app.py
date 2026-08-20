import streamlit as st
from components import load_css, page_header, stat_strip, module_card

st.set_page_config(
    page_title="Chlorograph — AI Agriculture Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

with st.sidebar:
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;'
        'font-size:1.15rem;color:var(--lime);">🌿 Chlorograph</div>'
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.68rem;'
        'color:var(--text-muted);margin-top:2px;">AI Agriculture Assistant · v1.0</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("Navigate using the pages above, or click a module card on this page.")

page_header(
    eyebrow="AI Agriculture Assistant · Precision Agronomy Capstone",
    title="Chlorograph — four models, one decision layer for your field.",
    subtitle=(
        "An end-to-end AI system that recommends what to plant, what to feed it, "
        "forecasts what it will yield, and reads the leaf when something's wrong — "
        "all served through a single FastAPI backend."
    ),
    accent_word="Chlorograph",
)

stat_strip([
    ("04", "Integrated Modules"),
    ("98.4%", "Disease Model Accuracy"),
    ("38", "Disease Classes Covered"),
    ("19", "Fertilizer Input Features"),
])

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Choose a module</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Each module is an independently trained model, unified behind one API. Click any card to open it.</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    module_card("🌾", "Module 01 · Tabular ML", "Crop Recommendation",
                "Suggests the best crop for a plot based on soil N-P-K, temperature, humidity, pH and rainfall.")
    if st.button("Open →", key="btn_crop", width='stretch'):
        st.switch_page("pages/1_Crop_Recommendation.py")

with col2:
    module_card("🧪", "Module 02 · Tabular ML", "Fertilizer Recommendation",
                "Recommends the optimal fertilizer from 19 soil, crop and environmental features.")
    if st.button("Open →", key="btn_fert", width='stretch'):
        st.switch_page("pages/2_Fertilizer_Recommendation.py")

with col3:
    module_card("📈", "Module 03 · Regression", "Crop Yield Prediction",
                "Forecasts expected yield (hg/ha) using historical climate and pesticide-use patterns.")
    if st.button("Open →", key="btn_yield", width='stretch'):
        st.switch_page("pages/3_Crop_Yield_Prediction.py")

with col4:
    module_card("🍃", "Module 04 · Deep Learning", "Disease Detection",
                "Upload a leaf photo — a fine-tuned EfficientNetB0 model flags the disease in seconds.")
    if st.button("Open →", key="btn_disease", width='stretch'):
        st.switch_page("pages/4_Disease_Prediction.py")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="text-align:center;color:var(--text-muted);font-family:\'IBM Plex Mono\',monospace;'
    'font-size:0.75rem;letter-spacing:0.05em;">'
    "BUILT WITH RANDOM FOREST · XGBOOST · EFFICIENTNETB0 · FASTAPI · STREAMLIT"
    "</div>",
    unsafe_allow_html=True,
)