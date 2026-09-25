import streamlit as st
from src.components.header import header_student_dashboard
from src.components.footer import footer_home
from src.components.subject_card import subject_card
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.dialog import enroll_subject
from src.middlewares.subject import get_enrolled_subjects_for_student
from src.database.db import get_student_attendance, get_subject_attendance_sessions, get_all_students, unenroll_student

def student_dashboard():
    style_base_layout()
    style_background_dashboard()
    header_student_dashboard()

    if 'login_toast' in st.session_state:
        st.toast(st.session_state.pop('login_toast'), icon="👋")

    student_id = st.session_state.get('student_id')
    student_name = st.session_state.get('student_data', 'Student')

    # Graceful recovery for dev server reloads if student_id is lost from session
    if not student_id and student_name:
        all_students = get_all_students() or []
        matched = [s for s in all_students if s.get('name') == student_name]
        if len(matched) == 1:
            student_id = matched[0].get('student_id')
            st.session_state['student_id'] = student_id

    st.subheader(f"Welcome to your Student Dashboard, {student_name}", text_alignment="center")
    st.space()

    col1, col2 = st.columns([4.7, 1.3], vertical_alignment="center")
    with col1:
        st.header("Enrolled Subjects", width="stretch")
    with col2:
        if st.button("Discover new Subjects", type="secondary", width=190, key="enroll_subject_btn"):
            enroll_subject()

    with st.spinner("Loading your Enrolled Subjects..."):
        subjects = get_enrolled_subjects_for_student(student_id)
        logs = get_student_attendance(student_id) if student_id else []

    stats_map = {}
    for log in logs:
        sid = log.get('subject_id')
        if sid is not None:
            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}
            if log.get('is_present', True):
                stats_map[sid]["attended"] += 1

    if subjects:
        for sub_node in subjects:
            sub = sub_node.get('subjects', sub_node)
            sid = sub.get('subject_id') or sub.get('id')
            if sid is not None:
                if sid not in stats_map:
                    stats_map[sid] = {"total": 0, "attended": 0}
                stats_map[sid]["total"] = get_subject_attendance_sessions(sid)

        def make_unenroll_btn(curr_sid, curr_code):
            def unenroll_btn():
                if st.button(
                    f"Unenroll from {curr_code}",
                    type="tertiary",
                    key=f"unenroll_{curr_sid}",
                    icon=":material/delete_forever:",
                    use_container_width=True,
                ):
                    unenroll_student(student_id, curr_sid)
                    st.toast(f"Unenrolled from {curr_code}")
                    st.rerun()
            return unenroll_btn

        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node.get('subjects', sub_node)
            sid = sub.get('subject_id') or sub.get('id')
            sub_code = sub.get('code') or sub.get('subject_code', '')
            stats = stats_map.get(sid, {'total': 0, 'attended': 0})
            percentage = f"{(stats['attended'] / stats['total'] * 100):.1f}%" if stats['total'] > 0 else "N/A"

            with cols[i % 2]:
                subject_card(
                    name=sub.get('name', 'Untitled Subject'),
                    code=sub_code,
                    section=sub.get('section', ''),
                    stats=[
                        ('🗓️', 'Total', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                        ('📊', 'Attendance', percentage),
                    ],
                    footer_callback=make_unenroll_btn(sid, sub_code)
                )
    else:
        st.info("You are not enrolled in any subjects yet. Click 'Discover new Subjects' to join a class.")

    st.divider()
    footer_home()