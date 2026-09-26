import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screens.student_screen import student_screen, student_screen_signup, student_face_login
from src.screens.student_screens.dashboard import student_dashboard
from src.screens.teacher_screens.teacher_screen import teacher_screen, teacher_screen_signup
from src.screens.teacher_screens.dashboard import teacher_dashboard
from src.screens.teacher_screens.take_attendence import take_attendence
from src.screens.teacher_screens.subjects import manage_subjects
from src.screens.teacher_screens.attendence import attendence_records
import importlib
import src.ui.base_layout
importlib.reload(src.ui.base_layout)
from src.ui.base_layout import style_base_layout
from src.components.dialog import auto_enroll
from src.utils.cookie_auth import get_cookie_manager, restore_session_from_cookie

def main():
    st.set_page_config(
        page_title = 'Snap Class - Faster Attendence using AI', 
        page_icon = "https://i.ibb.co/YTYGn5qV/logo.png"
    )

    style_base_layout()

    cookie_manager = get_cookie_manager()
    restore_session_from_cookie(cookie_manager)

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None

    join_code = st.query_params.get('join-code')
    is_student_logged_in = bool(st.session_state.get('student_id')) and st.session_state.get('user_role') == "student"

    if join_code:
        if is_student_logged_in:
            st.session_state["login_type"] = "student_dashboard"
        else:
            student_auth_views = {"student", "student_face_login", "student_screen_signup"}
            if st.session_state.get("login_type") not in student_auth_views:
                st.session_state["login_type"] = "student"

    match st.session_state["login_type"]:
        case "teacher":
            if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == "teacher":
                teacher_dashboard()
            else:
                teacher_screen()
        case "teacher_screen_signup":
            teacher_screen_signup()
        case "teacher_dashboard":
            teacher_dashboard()
        case "student":
            if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == "student":
                student_dashboard()
            else:
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

    if join_code and is_student_logged_in:
        auto_enroll(join_code)

if __name__ == "__main__":
    main()