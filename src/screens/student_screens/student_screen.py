import time
import streamlit as st
from PIL import Image
import numpy as np
from src.middlewares.student import register_student, login_student
from src.components.header import header_dashboard
from src.components.footer import footer_home
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.pipelines.face_pipeline import predict_attendence
from src.database.db import get_all_students

def student_screen():
    style_base_layout()
    style_background_dashboard()
    header_dashboard()
        
    st.header("Login to your Student Profile", text_alignment="center")
    st.space()
    student_email = st.text_input("Email id", placeholder="Enter your email id")
    student_password = st.text_input("Password", placeholder="Enter your password", type="password")
    st.divider()
    spacer, col1, col2, col3 = st.columns([1.5, 1, 1, 1], gap="small")
    with col1:
        if st.button("Login", type="primary", key="student_login", use_container_width=True):
            success, student, message = login_student(student_email, student_password)
            if success and student:
                student_id = student.get("student_id") if isinstance(student, dict) else student
                student_name = student.get("name", "Student") if isinstance(student, dict) else student
                st.session_state['student_id'] = student_id
                st.session_state['student_data'] = student_name
                st.session_state.user_role = "student"
                st.session_state['is_logged_in'] = True
                st.session_state['login_toast'] = message
                st.session_state['login_type'] = "student_dashboard"
                st.rerun()
            else:
                st.toast(icon="⚠️", body=message)
    with col2:
        if st.button("Login with FaceID", type="primary", key="student_login_faceid", use_container_width=True):
            st.session_state['login_type'] = "student_face_login"
            st.rerun()
    with col3:
        if st.button("Sign Up", type="secondary", key="student_signup", use_container_width=True):
            st.session_state['login_type'] = "student_screen_signup"
            st.rerun()
    
    footer_home()

def student_face_login():
    style_base_layout()
    style_background_dashboard()
    header_dashboard()

    st.header("Login with FaceID", text_alignment="center")
    st.space()
    photo = st.camera_input("Position your face in front of the camera")
    if photo:
        img = np.array(Image.open(photo))
        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendence(img)
            if num_faces == 0:
                st.warning("Face not found! Please ensure your face is clearly visible to the camera.")
            elif num_faces > 1:
                st.warning("Multiple faces found! Please ensure only one person is in front of the camera.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students() or []
                    student = next((s for s in all_students if str(s.get('student_id')) == str(student_id)), None)
                    if student:
                        actual_student_id = student.get('student_id')
                        student_name = student.get('name', 'Student')
                        st.session_state['student_id'] = actual_student_id
                        st.session_state['student_data'] = student_name
                        st.session_state.user_role = "student"
                        st.session_state['is_logged_in'] = True
                        st.session_state['login_type'] = "student_dashboard"
                        st.session_state['login_toast'] = "Welcome Back, " + student_name
                        st.rerun()
                    else:
                        st.toast("Face matched ID but student profile was not found in database. Please sign up or contact support.", icon="⚠️")
                        st.error("Face matched ID but student profile was not found in database. Please sign up or contact support.")
                else:
                    st.toast(icon="⚠️", body="Face Not Recognized! Sign up with Snap Class")
                    st.session_state['auth_toast'] = "Face Not Recognized! Sign up with Snap Class"
                    time.sleep(2)
                    st.session_state['login_type'] = "student_screen_signup"
                    st.rerun()

    footer_home()

def student_screen_signup():
    style_base_layout()
    style_background_dashboard()
    header_dashboard()

    if 'auth_toast' in st.session_state:
        st.toast(st.session_state.pop('auth_toast'), icon="⚠️")

    st.header("Register your Student Profile", text_alignment="center")
    st.space()
    student_name = st.text_input("Name", placeholder="Enter your name")
    student_email = st.text_input("Email id", placeholder="Enter your email id")
    student_password = st.text_input("Password", placeholder="Enter your password", type="password")
    student_confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
    audio = None
    try:
        audio = st.audio_input("Record Audio for Voice only attendance (Optional)")
    except Exception as e:
        st.toast(icon="⚠️", body="Audio Recording Failed")

    img = None
    photo = st.camera_input("Position your face in front of the camera")
    if photo:
        img = np.array(Image.open(photo))
    st.divider()
    if st.button("Sign up", type="secondary", key="student_signup_submit", use_container_width=True):
        if img is None:
            st.toast(icon="⚠️", body="Please capture a photo of your face before signing up.")
        else:
            success, student_id, message = register_student(student_name, student_email, student_password, student_confirm_password, img, audio)
            if success:
                st.session_state['student_id'] = student_id
                st.session_state['student_data'] = student_name
                st.session_state.user_role = "student"
                st.session_state['is_logged_in'] = True
                st.session_state['login_type'] = "student_dashboard"
                st.session_state['login_toast'] = message
                st.rerun()
            else:
                st.toast(icon="⚠️", body=message)

    footer_home()