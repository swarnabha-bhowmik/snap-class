import streamlit as st
import textwrap

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""<div style="text-align: center; margin-bottom: 1rem;">
<img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px; display: block; margin: 0 auto 8px auto;">
<h1 class="brand-title" style="text-align: center !important; color: #E0E3FF !important; font-family: 'Climate Crisis', sans-serif !important; font-variation-settings: 'YEAR' 1979 !important; font-size: 3.5rem !important; font-weight: 400 !important; line-height: 1.05 !important; margin: 0 auto !important;">SNAP<br>CLASS</h1>
</div>""",
        unsafe_allow_html=True
    )

def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    col_back, col_brand, col_spacer = st.columns([2.0, 2.8, 1.2], vertical_alignment="center")
    
    with col_back:
        if st.button("← Back to Home", type="secondary", key="auth_back_home", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    with col_brand:
        st.markdown(
            f"""<div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 auto; text-align: left;">
<img src="{logo_url}" alt="Logo" style="width: 56px; height: 48px; object-fit: contain; margin: 0; display: block;">
<h2 class="brand-title dashboard-brand-title" style="color: #5865F2 !important; font-family: 'Climate Crisis', sans-serif !important; font-variation-settings: 'YEAR' 1979 !important; font-size: 1.85rem !important; font-weight: 400 !important; line-height: 1.05; margin: 0 !important; padding: 0; text-align: left; display: inline-block;">SNAP<br>CLASS</h2>
</div>""",
            unsafe_allow_html=True
        )

def header_teacher_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    col_back, col_brand, col_logout = st.columns([2.3, 2.6, 1.1], vertical_alignment="center")
    
    with col_back:
        if st.button("← Back to Dashboard", type="secondary", key="teacher_back_dashboard", use_container_width=True):
            st.session_state['login_type'] = "teacher_dashboard"
            st.rerun()

    with col_brand:
        st.markdown(
            f"""<div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 auto; text-align: left;">
<img src="{logo_url}" alt="Logo" style="width: 56px; height: 48px; object-fit: contain; margin: 0; display: block;">
<h2 class="brand-title dashboard-brand-title" style="color: #5865F2 !important; font-family: 'Climate Crisis', sans-serif !important; font-variation-settings: 'YEAR' 1979 !important; font-size: 1.85rem !important; font-weight: 400 !important; line-height: 1.05; margin: 0 !important; padding: 0; text-align: left; display: inline-block;">SNAP<br>CLASS</h2>
</div>""",
            unsafe_allow_html=True
        )
    with col_logout:
        if st.button("Logout", type="primary", key="teacher_logout", use_container_width=True):
            st.session_state['login_type'] = None
            st.session_state.pop('teacher_data', None)
            st.session_state.pop('user_role', None)
            st.rerun()

def header_student_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    col_back, col_brand, col_logout = st.columns([2.0, 2.8, 1.2], vertical_alignment="center")
    
    with col_back:
        if st.button("← Back to Home", type="secondary", key="student_back_home", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    with col_brand:
        st.markdown(
            f"""<div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 auto; text-align: left;">
<img src="{logo_url}" alt="Logo" style="width: 56px; height: 48px; object-fit: contain; margin: 0; display: block;">
<h2 class="brand-title dashboard-brand-title" style="color: #5865F2 !important; font-family: 'Climate Crisis', sans-serif !important; font-variation-settings: 'YEAR' 1979 !important; font-size: 1.85rem !important; font-weight: 400 !important; line-height: 1.05; margin: 0 !important; padding: 0; text-align: left; display: inline-block;">SNAP<br>CLASS</h2>
</div>""",
            unsafe_allow_html=True
        )
    with col_logout:
        if st.button("Logout", type="primary", key="student_logout", use_container_width=True):
            st.session_state['login_type'] = None
            st.session_state.pop('student_data', None)
            st.session_state.pop('student_id', None)
            st.session_state.pop('user_role', None)
            st.rerun()