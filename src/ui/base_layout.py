import streamlit as st

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
        </style>
    """, unsafe_allow_html = True)

def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:wght@200..800&display=swap');
            
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
            [data-testid="stMarkdownContainer"] span,
            p, span, label, input, textarea, select
            {
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
            }

            /* Brand / App Main Header */
            h1, h1 *, .brand-title, .brand-title *,
            [data-testid="stHeading"] h1,
            [data-testid="stHeading"] h1 *
            {
                font-family: "Climate Crisis" !important;
                font-weight: 400 !important;
                font-size: 3.5rem !important;
                line-height: 1.05 !important;
                margin-bottom: 0rem !important;
                color: #E0E3FF !important;
                text-align: center !important;
            }

            /* Section Headers */
            h2:not(.brand-title),
            h2:not(.brand-title) *,
            [data-testid="stHeading"] h2,
            [data-testid="stHeading"] h2 *
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

            h4, h5, h6
            {
                font-family: "Outfit", sans-serif !important;
            }

            /* Buttons & Button text */
            button,
            button *,
            .stButton > button,
            .stButton > button *,
            [data-testid^="stBaseButton"],
            [data-testid^="stBaseButton"] *
            {
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: 0.02em !important;
            }

            button,
            .stButton > button
            {
                background: #5865F2 !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button p,
            .stButton > button p
            {
                color: white !important;
                font-family: "Outfit", "Plus Jakarta Sans", sans-serif !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                margin: 0 !important;
            }

            button[kind="secondary"],
            .stButton > button[kind="secondary"]
            {
                background: #EB459E !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="tertiary"],
            .stButton > button[kind="tertiary"]
            {
                background: black !important;
                border-radius: 1.5rem !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button:hover,
            .stButton > button:hover
            {
                transform: scale(1.05) !important;
            }

            h1.brand-title,
            h1.brand-title *
            {
                font-family: "Climate Crisis" !important;
                font-weight: 400 !important;
            }
        </style>
    """, unsafe_allow_html = True)
