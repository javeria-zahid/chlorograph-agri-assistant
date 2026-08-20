"""
Shared styling + component helpers used by every page in the dashboard.
Import from here instead of repeating markdown/CSS in each page file.
"""

import streamlit as st
from pathlib import Path

CSS_PATH = Path(__file__).parent / "assets" / "style.css"


def load_css():
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def page_header(eyebrow: str, title: str, subtitle: str, accent_word: str | None = None):
    """Renders the eyebrow + title + subtitle block used at the top of every page."""
    if accent_word and accent_word in title:
        title_html = title.replace(accent_word, f'<span class="accent">{accent_word}</span>')
    else:
        title_html = title

    html = (
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<div class="display-title">{title_html}</div>'
        f'<div class="subtitle">{subtitle}</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def stat_strip(stats: list[tuple[str, str]]):
    """stats = [(value, label), ...]"""
    items = "".join(
        f'<div class="stat-item"><div class="stat-value">{v}</div>'
        f'<div class="stat-label">{l}</div></div>'
        for v, l in stats
    )
    st.markdown(f'<div class="stat-strip">{items}</div>', unsafe_allow_html=True)


def module_card(icon: str, tag: str, title: str, desc: str):
    html = (
        f'<div class="module-card">'
        f'<div class="module-icon">{icon}</div>'
        f'<div class="module-tag">{tag}</div>'
        f'<div class="module-title">{title}</div>'
        f'<div class="module-desc">{desc}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def result_card(label: str, value: str, tone: str = "success", note: str | None = None, confidence: float | None = None):
    """tone: 'success' or 'warning'"""
    value_class = "lime" if tone == "success" else "danger"
    note_html = f'<div style="margin-top:10px;color:var(--text-muted);font-size:0.85rem;">{note}</div>' if note else ""
    conf_html = ""
    if confidence is not None:
        pct = round(confidence * 100, 1)
        conf_html = (
            f'<div class="confidence-bar-track"><div class="confidence-bar-fill" style="width:{pct}%;"></div></div>'
            f'<div style="margin-top:6px;font-family:\'IBM Plex Mono\',monospace;font-size:0.78rem;color:var(--text-muted);">'
            f'confidence: {pct}%</div>'
        )
    html = (
        f'<div class="result-card {tone}">'
        f'<div class="result-label">{label}</div>'
        f'<div class="result-value {value_class}">{value}</div>'
        f'{conf_html}{note_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def empty_state(icon: str, text: str):
    html = f'<div class="empty-state"><div class="icon">{icon}</div><div>{text}</div></div>'
    st.markdown(html, unsafe_allow_html=True)


API_BASE_URL = "http://127.0.0.1:8000"
API_BASE_URL = "http://127.0.0.1:8000"
