import streamlit as st
from src.components.header import header_teacher_dashboard
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_dashboard

def teacher_dashboard():
    style_base_layout()
    style_background_dashboard()
    header_teacher_dashboard()

    teacher_data = st.session_state.teacher_data
    st.subheader(f"""Welcome to your Teacher Dashboard, {teacher_data}""", text_alignment = "center")
    st.space()

    tab1, tab2, tab3 = st.columns(3)
    with tab1:
        if st.button("Take Attendence", type="primary", width="stretch", icon=":material/face:"):
            st.session_state['login_type'] = "take_attendence"
            st.rerun()
    with tab2:
        if st.button("Manage Subjects", type="primary", width="stretch", icon=":material/library_books:"):
            st.session_state['login_type'] = "manage_subjects"
            st.rerun()
    with tab3:
        if st.button("Attendence Records", type="primary", width="stretch", icon=":material/assignment:"):
            st.session_state['login_type'] = "attendence_records"
            st.rerun()

    footer_home()