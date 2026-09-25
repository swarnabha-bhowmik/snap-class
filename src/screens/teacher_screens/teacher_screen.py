import streamlit as st
from src.components.footer import footer_home
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.middlewares.teacher import register_teacher, login_teacher

def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    header_dashboard()
    
    st.header("Login to your Teacher Profile", text_alignment="center")
    st.space()
    teacher_username = st.text_input("Username", placeholder="Enter your username")
    teacher_password = st.text_input("Password", placeholder="Enter your password", type="password")
    st.divider()
    spacer, col1, col2 = st.columns([2.5, 1, 1], gap="small")
    with col1:
        if st.button("Login", type="primary", key="teacher_login", use_container_width=True):
            success, message = login_teacher(teacher_username, teacher_password)
            if success:
                st.toast(message)
                st.session_state['teacher_data'] = teacher_username
                st.session_state['login_type'] = "teacher_dashboard"
                st.rerun()
            else:
                st.toast(icon="⚠️", body=message)
    with col2:
        if st.button("Sign Up", type="secondary", key="teacher_signup", use_container_width=True):
            st.session_state['login_type'] = "teacher_screen_signup"
            st.rerun()

    footer_home()

def teacher_screen_signup():
    style_base_layout()
    style_background_dashboard()
    header_dashboard()

    st.header("Register your Teacher Profile", text_alignment="center")
    st.space()
    teacher_name = st.text_input("Full Name", placeholder="Enter your full name")
    teacher_username = st.text_input("Username", placeholder="Enter your username")
    teacher_password = st.text_input("Password", placeholder="Enter your password", type="password")
    teacher_confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
    st.divider()
    if st.button("Sign up", type="secondary", key="teacher_signup_submit", use_container_width=True):
        success, message = register_teacher(teacher_name, teacher_username, teacher_password, teacher_confirm_password)
        if success:
            st.session_state['login_type'] = "teacher"
            st.session_state['teacher_data'] = teacher_username
            st.toast(message)
            st.rerun()
        else:
            st.toast(icon="⚠️", body=message)

    footer_home()