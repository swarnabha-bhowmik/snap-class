import streamlit as st
from src.components.header import header_teacher_dashboard
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.dialog import create_subject, share_subject
from src.database.db import get_subjects
from src.components.subject_card import subject_card

def manage_subjects():
    style_base_layout()
    style_background_dashboard()
    header_teacher_dashboard()
    
    teacher_data = st.session_state.get('teacher_data', '')
    teacher_username = teacher_data['teacher_username'] if isinstance(teacher_data, dict) else teacher_data
    st.space()
    col1, col2 = st.columns([3.6, 2.4], vertical_alignment="center")
    with col1:
        st.header("Manage Subjects", width="stretch")
    with col2:
        if st.button("Create New Subject", type="secondary", use_container_width=True, key="create_new_sub_btn"):
            create_subject(teacher_username)
    
    subjects = get_subjects(teacher_username)
    if subjects:
        for sub in subjects:
            sub_name = sub.get("name", "")
            sub_code = sub.get("code") or sub.get("subject_code", "")
            sub_section = sub.get("section", "")
            stats = [
                ("👥", "Students", sub.get("total_students", 0)),
                ("🕰️", "Classes", sub.get("total_classes", 0)),
            ]
            def make_share_btn(name, code):
                def share_btn():
                    if st.button(f"Share Code: {code}", key=f"share_{code}", icon=":material/share:"):
                        share_subject(name, code)
                    st.space()
                return share_btn

            subject_card(
                name=sub_name,
                code=sub_code,
                section=sub_section,
                stats=stats,
                footer_callback=make_share_btn(sub_name, sub_code)
            )
    else:
        st.toast(icon="⚠️", body="No subjects found")
        
    footer_home()