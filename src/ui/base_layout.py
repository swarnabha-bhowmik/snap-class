import base64
from pathlib import Path
import streamlit as st

CLIMATE_CRISIS_WOFF2_URL = (
    "https://fonts.gstatic.com/s/climatecrisis/v15/wEOkEB3AntNeKCPBVW9XOKlmp1oYqbY.woff2"
)

@st.cache_data
def get_climate_crisis_base64() -> str:
    font_path = Path(__file__).parent.parent / "assets" / "fonts" / "ClimateCrisis.woff2"
    if font_path.exists():
        with open(font_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def _inject_css(css: str) -> None:
    html = f"<style>{css}</style>"
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)

def style_background_home():
    st.markdown("""
        <style>
            .stApp,
            [data-testid="stAppViewContainer"]
            {
                background-color: #5865F2 !important;
            }
            .stApp div[data-testid="stColumn"]
            {
                background-color: #E0E3FF !important;
                padding: 1.5rem !important;
                border-radius: 5rem !important;
            }
        </style>
    """, unsafe_allow_html = True)

def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp,
            [data-testid="stAppViewContainer"]
            {
                background-color: #E0E3FF !important;
            }
            .stApp div[data-testid="stColumn"]
            {
                background-color: transparent !important;
                padding: 0 !important;
                border-radius: 0 !important;
            }
        </style>
    """, unsafe_allow_html = True)

def style_base_layout():
    font_b64 = get_climate_crisis_base64()
    local_src = (
        f"url('data:font/woff2;base64,{font_b64}') format('woff2'), "
        if font_b64
        else ""
    )
    _inject_css(f"""
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979..2050&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:wght@200..800&display=swap');

        @font-face {{
            font-family: 'Climate Crisis';
            font-style: normal;
            font-weight: 400;
            font-display: swap;
            src: {local_src}url('{CLIMATE_CRISIS_WOFF2_URL}') format('woff2');
        }}
    """)

    _inject_css("""
            
            #MainMenu,
            footer,
            header
            {
                visibility: hidden;
            }

            [data-testid="stMainBlockContainer"]
            {
                padding-top: 1.5rem !important;
            }

            /* Global typography */
            html, body, .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stMarkdownContainer"] p,
            p, label, input, textarea, select
            {
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
            }

            [data-testid="stWidgetLabel"],
            [data-testid="stWidgetLabel"] *
            {
                color: #111827 !important;
                font-weight: 600 !important;
            }

            [data-testid="stMarkdownContainer"] hr
            {
                border-color: #5865F2 !important;
                opacity: 1 !important;
            }

            /* Brand / App Main Header */
            [data-testid="stMarkdownContainer"] h1.brand-title,
            [data-testid="stMarkdownContainer"] h1.brand-title *,
            [data-testid="stMarkdownContainer"] h2.brand-title,
            [data-testid="stMarkdownContainer"] h2.brand-title *,
            h1.brand-title,
            h1.brand-title *,
            h2.brand-title,
            h2.brand-title *,
            .brand-title,
            .brand-title *,
            .dashboard-brand-title,
            .dashboard-brand-title *
            {
                font-family: "Climate Crisis", sans-serif !important;
                font-variation-settings: "YEAR" 1979 !important;
                font-synthesis: none !important;
                font-weight: 400 !important;
            }

            [data-testid="stMarkdownContainer"] h1.brand-title,
            h1.brand-title
            {
                font-size: 3.5rem !important;
                line-height: 1.05 !important;
                margin-bottom: 0rem !important;
                color: #E0E3FF !important;
                text-align: center !important;
            }

            /* Section Headers */
            h2:not(.brand-title):not(.dashboard-brand-title),
            h2:not(.brand-title):not(.dashboard-brand-title) *,
            [data-testid="stHeading"] h2:not(.brand-title),
            [data-testid="stHeading"] h2:not(.brand-title) *
            {
                font-family: "Outfit" !important;
                font-weight: 600 !important;
                color: black !important;
                font-size: 2rem !important;
                line-height: 1.25 !important;
            }

            h3:not(.brand-title),
            h3:not(.brand-title) *,
            [data-testid="stHeading"] h3,
            [data-testid="stHeading"] h3 *
            {
                font-family: "Outfit", sans-serif !important;
                color: black !important;
                font-size: 1.5rem !important;
                line-height: 1.25 !important;
            }

            h2.page-title,
            h2.page-title *
            {
                font-family: "Climate Crisis", sans-serif !important;
                font-variation-settings: "YEAR" 1979 !important;
                font-weight: 400 !important;
                color: #5865F2 !important;
                font-size: 2rem !important;
                line-height: 1.15 !important;
                margin: 1rem 0 1.5rem !important;
                text-align: center !important;
            }

            h4, h5, h6
            {
                font-family: "Outfit", sans-serif !important;
            }

            /* Buttons & Button text */
            .stButton > button,
            .stButton > button *:not([data-testid="stIconMaterial"]):not([data-testid="stIconMaterial"] *)
            {
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: 0.02em !important;
            }

            [data-testid="stIconMaterial"],
            [data-testid="stIconMaterial"] *
            {
                font-family: "Material Symbols Rounded" !important;
                font-weight: normal !important;
                font-style: normal !important;
                letter-spacing: normal !important;
                text-transform: none !important;
            }

            .stButton > button
            {
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                min-height: 44px !important;
                height: auto !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 6px 12px !important;
                gap: 6px !important;
                border: none !important;
                box-sizing: border-box !important;
                transition: transform 0.25s ease-in-out, background 0.25s ease-in-out !important;
            }

            .stButton > button [data-testid="stIconMaterial"]
            {
                font-size: 1.2rem !important;
                flex-shrink: 0 !important;
                margin-right: 2px !important;
            }

            .stButton > button span[data-has-shortcut="true"]
            {
                display: inline-flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 6px !important;
            }

            .stButton > button kbd
            {
                font-family: inherit !important;
                font-size: 0.65rem !important;
                font-weight: 500 !important;
                padding: 2px 6px !important;
                margin: 0 !important;
                line-height: 1 !important;
                border-radius: 4px !important;
                background: rgba(255, 255, 255, 0.2) !important;
                border: 1px solid rgba(255, 255, 255, 0.4) !important;
                color: white !important;
                white-space: nowrap !important;
            }

            button p,
            .stButton > button p,
            .stButton > button div,
            .stButton > button div[data-testid="stMarkdownContainer"]
            {
                color: white !important;
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.88rem !important;
                line-height: 1.25 !important;
                margin: 0 !important;
                white-space: nowrap !important;
                overflow: visible !important;
                text-overflow: clip !important;
                max-width: none !important;
            }

            /* Primary Buttons */
            .stButton > button[kind="primary"],
            .stButton > button[data-testid="stBaseButton-primary"],
            .stButton > button:not([kind="secondary"]):not([kind="tertiary"]):not([data-testid="stBaseButton-secondary"]):not([data-testid="stBaseButton-tertiary"])
            {
                background: #5865F2 !important;
                background-color: #5865F2 !important;
                color: white !important;
            }

            .stButton > button[kind="primary"]:hover,
            .stButton > button[data-testid="stBaseButton-primary"]:hover
            {
                background: #4752C4 !important;
                background-color: #4752C4 !important;
            }

            /* Secondary Buttons */
            .stButton > button[kind="secondary"],
            .stButton > button[data-testid="stBaseButton-secondary"],
            button[kind="secondary"],
            button[data-testid="stBaseButton-secondary"],
            button[data-testid="baseButton-secondary"]
            {
                background: #EB459E !important;
                background-color: #EB459E !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 8px 16px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out, background 0.25s ease-in-out !important;
            }

            .stButton > button[kind="secondary"]:hover,
            .stButton > button[data-testid="stBaseButton-secondary"]:hover,
            button[kind="secondary"]:hover,
            button[data-testid="stBaseButton-secondary"]:hover
            {
                background: #D83A8F !important;
                background-color: #D83A8F !important;
            }

            .stButton > button[kind="secondary"] p,
            .stButton > button[data-testid="stBaseButton-secondary"] p,
            button[kind="secondary"] p,
            button[data-testid="stBaseButton-secondary"] p
            {
                color: white !important;
            }

            /* Specific button by key (e.g. key="teacher_signup") */
            .st-key-teacher_signup .stButton > button,
            .st-key-teacher_signup button
            {
                background: #EB459E !important;
                background-color: #EB459E !important;
                color: white !important;
            }

            .st-key-teacher_signup .stButton > button:hover,
            .st-key-teacher_signup button:hover
            {
                background: #D83A8F !important;
                background-color: #D83A8F !important;
            }

            .st-key-teacher_signup .stButton > button p,
            .st-key-teacher_signup button p
            {
                color: white !important;
            }

            /* Tertiary Buttons */
            .stButton > button[kind="tertiary"],
            button[kind="tertiary"]
            {
                background: black !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            .stButton > button:hover
            {
                transform: scale(1.05) !important;
            }

            h1.brand-title,
            h1.brand-title *
            {
                font-family: "Climate Crisis", sans-serif !important;
                font-variation-settings: "YEAR" 1979 !important;
                font-weight: 400 !important;
                color: #E0E3FF !important;
            }

            h2.brand-title,
            h2.brand-title *,
            .dashboard-brand-title,
            .dashboard-brand-title *
            {
                font-family: "Climate Crisis", sans-serif !important;
                font-variation-settings: "YEAR" 1979 !important;
                font-weight: 400 !important;
                color: #5865F2 !important;
            }
    """)
