import streamlit as st
from src.components.footer import footer_home
from src.ui.base_layout import style_background_dashboard, style_base_layout

def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    
    if st.button("← Back to Home", type="secondary"):
        st.session_state['login_type'] = None
        st.rerun()
        
    st.header("Teacher Dashboard")
    st.write("Welcome to the Teacher Portal. Class attendance and logs will appear here.")
    
    footer_home()