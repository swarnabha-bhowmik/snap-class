import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_background_home, style_base_layout

def home_screen():
    style_background_home()
    style_base_layout()
    header_home()
    col1, col2, = st.columns(2, gap="large")
    with col1:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=120)
        if st.button("Teacher Portal", type="secondary", key="home_teacher_portal"):
            if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == "teacher":
                st.session_state['login_type'] = "teacher_dashboard"
            else:
                st.session_state['login_type'] = "teacher"
            st.rerun()
    with col2:
        st.header("I'm Student")
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
        if st.button("Student Portal", type="secondary", key="home_student_portal"):
            if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == "student":
                st.session_state['login_type'] = "student_dashboard"
            else:
                st.session_state['login_type'] = "student"
            st.rerun()
    
    footer_home()