import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from src.components.header import header_teacher_dashboard
from src.components.footer import footer_home
from src.components.dialog import add_photos, attendence_result, voice_attendence
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.database.config import supabase
from src.database.db import get_subjects
from src.pipelines.face_pipeline import predict_attendence

def take_attendence():
    style_base_layout()
    style_background_dashboard()
    header_teacher_dashboard()
    
    st.header("Take AI Attendence")
    st.space()
    teacher_data = st.session_state.get('teacher_data', '')
    teacher_username = teacher_data['teacher_username'] if isinstance(teacher_data, dict) else teacher_data
    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []
    subjects = get_subjects(teacher_username)
    if not subjects:
        st.toast(icon="⚠️", body="No subject found")
        return
    subject_options = {f"{s['name']} — {s.get('code') or s.get('subject_code', '')}": s['subject_id'] for s in subjects}

    col1, col2, col3 = st.columns([3,1,1], vertical_alignment='bottom')
    with col1:
        selected_label = st.selectbox("Select Subject", options=list(subject_options.keys()))
    with col2:
        if st.button("Add Photos", type="secondary", icon=":material/photo_prints:", width="stretch"):
            add_photos()
    selected_subject_id = subject_options[selected_label]
    with col3:
        if st.button("Run Voice Analysis", type="primary", width='stretch', icon=":material/mic:"):
            st.session_state.voice_review_data = None
            enrolled_res = supabase.table('subject_student').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            if not enrolled_res.data:
                st.toast(icon="⚠️", body="No students have enrolled in this subject")
            else:
                voice_attendence(selected_subject_id, enrolled_res.data)
    st.divider()

    if st.session_state.attendence_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for id, img in enumerate(st.session_state.attendence_images):
            with gallery_cols[id % 4]:
                st.image(img, width='stretch', caption=f"Photo {id+1}")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Clear All Photos", type="tertiary", width='stretch', icon=":material/delete:"):
                st.session_state.attendence_images = []
                st.rerun()
        with c2:
            if st.button("Run Face Analysis", type="secondary", width='stretch', icon=":material/analytics:"):
                with st.spinner("Face Analysis in progress..."):
                    all_detected = {}
                    for id, img in enumerate(st.session_state.attendence_images):
                        img_np = np.array(img.convert("RGB"))
                        detected, _, _ = predict_attendence(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected.setdefault(student_id, []).append(f"Photo {id+1}")
                    enrolled_res = supabase.table('subject_student').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                    if not enrolled_res.data:
                        st.toast(icon="⚠️", body="No student have enrolled in this subject")
                    else:
                        res, attendence = [], []
                        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                        for node in enrolled_res.data:
                            student = node['students']
                            sources = all_detected.get(int(student['student_id']), [])
                            is_present = len(sources) > 0
                            res.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "—",
                                "Status": "✅ Present" if is_present else "❌ Absent"
                            })
                            attendence.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamps': timestamp,
                                'is_present': bool(is_present)
                            })
                    attendence_result(pd.DataFrame(res), attendence)

    footer_home()