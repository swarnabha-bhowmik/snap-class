import streamlit as st
import textwrap

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        textwrap.dedent(f"""
            <div style="text-align: center; margin-bottom: 1rem;">
                <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px; display: block; margin: 0 auto 8px auto;">
                <h1 class="brand-title" style="text-align: center; color: #E0E3FF; font-family: 'Climate Crisis', sans-serif; font-size: 3.5rem; font-weight: 400 !important; line-height: 1.05; margin: 0 auto;">SNAP<br>CLASS</h1>
            </div>
        """),
        unsafe_allow_html=True
    )