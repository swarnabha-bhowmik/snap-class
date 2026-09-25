import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screens.student_screen import student_screen, student_screen_signup, student_face_login
from src.screens.student_screens.dashboard import student_dashboard
from src.screens.teacher_screens.teacher_screen import teacher_screen, teacher_screen_signup
from src.screens.teacher_screens.dashboard import teacher_dashboard
from src.screens.teacher_screens.take_attendence import take_attendence
from src.screens.teacher_screens.subjects import manage_subjects
from src.screens.teacher_screens.attendence import attendence_records
from src.screens.teacher_screens.dashboard import teacher_dashboard
import importlib
import src.ui.base_layout
importlib.reload(src.ui.base_layout)
from src.ui.base_layout import style_base_layout
from src.components.dialog import auto_enroll

def main():
    st.set_page_config(
        page_title = 'Snap Class - Faster Attendence using AI', 
        page_icon = "https://i.ibb.co/YTYGn5qV/logo.png"
    )

    style_base_layout()

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()
        case "teacher_screen_signup":
            teacher_screen_signup()
        case "teacher_dashboard":
            teacher_dashboard()
        case "student":
            student_screen()
        case "student_screen_signup":
            student_screen_signup()
        case "student_face_login":
            student_face_login()
        case "student_dashboard":
            student_dashboard()
        case "take_attendence":
            take_attendence()
        case "manage_subjects":
            manage_subjects()
        case "attendence_records":
            attendence_records()
        case None:
            home_screen()

    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != "student":
            st.session_state.login_type = "student"
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == "student":
            auto_enroll(join_code)

if __name__ == "__main__":
    main()