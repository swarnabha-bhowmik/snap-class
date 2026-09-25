import streamlit as st
import pandas as pd
from src.middlewares.subject import check_subject, check_enroll
import segno
import io
from src.database.config import supabase
from src.database.db import is_student_enrolled, enroll_student, create_attendence
import time
from PIL import Image
from src.pipelines.voice_pipeline import process_bulk_audio
from datetime import datetime

@st.dialog("Create New Subject")
def create_subject(teacher_username):
    st.write("Enter the details of new subject")
    st.space()
    sub_id = st.text_input("Subject Code", placeholder="Enter the subject code")
    sub_name = st.text_input("Subject Name", placeholder="Enter the subject name")
    sub_section = st.text_input("Section", placeholder="Enter the section")
    st.divider()
    if st.button("Create Subject", type="secondary", use_container_width=True):
        success, message = check_subject(sub_id, sub_name, sub_section, teacher_username)
        if success:
            st.toast(body=message)
            st.rerun()
        else:
            st.toast(icon="⚠️", body=message)
        
@st.dialog("Share Class Link")
def share_subject(subject_name, subject_code):
    app_domain = st.secrets.get("APP_DOMAIN", "http://localhost:8501")
    join_url = f"{app_domain}/?join-code={subject_code}"
    st.header("Scan to Join")
    qr = segno.make(join_url)
    buff = io.BytesIO()
    qr.save(buff, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.toast(body="Copy the link to share your classes")
    with col2:
        st.markdown("### Scan to Join")
        st.image(buff.getvalue(), use_container_width=True, caption="QR Code for class joining")

@st.dialog("Enroll in Subject")
def enroll_subject():
    code = st.text_input("Subject Code", placeholder="Enter the subject code")
    if st.button("Enroll now", type="primary", use_container_width=True):
        student_id = st.session_state.get('student_id')
        success, message = check_enroll(code, student_id=student_id)
        if success:
            st.toast(body=message)
            st.rerun()
        else:
            st.toast(icon="⚠️", body=message)

@st.dialog("Quick Enrollment")
def auto_enroll(code):
    student_data = st.session_state.get('student_data')
    student_id = st.session_state.get('student_id')
    if not student_id and isinstance(student_data, dict):
        student_id = student_data.get('student_id')
    res = supabase.table('subjects').select('subject_id', 'name').eq('code', code).execute()
    if not res.data:
        st.error("Could not find a subject matching this QR code.")
        if st.button("Close", type="tertiary", use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]
    if is_student_enrolled(student_id, subject['subject_id']):
        st.info(f"You are already enrolled in **{subject['name']}**.")
        if st.button("Close", type="primary", use_container_width=True):
            st.query_params.clear()
            st.rerun()
        return
    
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Enroll", type="primary", use_container_width=True):
            result = enroll_student(student_id, subject['subject_id'])
            if result:
                st.toast(f"Successfully joined {subject['name']}!", icon="🎉")
            else:
                st.toast(icon="⚠️", body="Some Error Occurred, Try Again later")
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("No, Cancel", type="tertiary", use_container_width=True):
            st.query_params.clear()
            st.rerun()

@st.dialog("Add Photos")
def add_photos():
    st.write("Add classroom photos for attendence")
    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []

    tab_cam, tab_upload = st.tabs(["📷 Camera", "📁 Upload"])
    with tab_cam:
        img = st.camera_input("Take Snapshot", key="dialog_cam")
        if img:
            st.session_state.attendence_images.append(Image.open(img))
            st.toast("Photo added successfully")
            st.rerun()
    with tab_upload:
        imgs = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key="dialog_upload")
        if imgs:
            for uploaded_file in imgs:
                st.session_state.attendence_images.append(Image.open(uploaded_file))
            st.toast("Photo(s) uploaded successfully")
            st.rerun()
    st.divider()
    if st.button("Done", type="secondary", use_container_width=True):
        st.rerun()

@st.dialog("Attendence Report")
def attendence_result(df, logs):
    st.write("Review before confirming")
    st.dataframe(df, hide_index=True, width="stretch")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", type="tertiary", width="stretch"):
            st.rerun()
    with col2:
        if st.button("Confirm", type="primary", key="confirm_attendence_btn", width="stretch"):
            try:
                create_attendence(logs)
                st.toast(body="Attendence Taken")
                st.session_state.attendence_images = []
                st.rerun()
            except Exception as e:
                st.toast(icon="⚠️", body=f"Sync Failed: {str(e)}")  
                st.rerun()

@st.dialog("Voice Attendence")
def voice_attendence(selected_subject_id, enrolled_res):
    st.write("Record classroom audio to detect student voices")
    audio = st.audio_input("Record audio")

    if st.button("Analyse Audio", type="primary", width="stretch", key="analyse_audio_btn"):
        if not audio:
            st.toast(icon="⚠️", body="Please record audio before analyzing.")
        else:
            with st.spinner("Processing voice analysis..."):
                nodes = enrolled_res if isinstance(enrolled_res, list) else enrolled_res.data
                candidates_dict = {
                    s['students']['student_id'] : s['students']['voice_embedding']
                    for s in nodes if s.get('students') and s['students'].get('voice_embedding')
                }
                if not candidates_dict:
                    st.toast(icon="⚠️", body="None of the enrolled students had their voice recorded")
                else:
                    audio_bytes = audio.read()
                    all_detected = process_bulk_audio(audio_bytes, candidates_dict) or {}

                    res, attendence = [], []
                    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in nodes:
                        student = node['students']
                        sid = student['student_id']
                        score = all_detected.get(sid) or all_detected.get(str(sid), 0.0)
                        is_present = bool(score > 0)
                        res.append({
                            "Name": student['name'],
                            "ID": sid,
                            "Score": f"{score:.2f}" if is_present else "—",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })
                        attendence.append({
                            'student_id': sid,
                            'subject_id': selected_subject_id,
                            'timestamps': timestamp,
                            'is_present': bool(is_present)
                        })

                    st.session_state['voice_review_data'] = {
                        'df': pd.DataFrame(res),
                        'logs': attendence
                    }

    if st.session_state.get('voice_review_data'):
        review_data = st.session_state['voice_review_data']
        st.divider()
        st.subheader("Attendence Report")
        st.write("Review detected attendance before confirming:")
        st.dataframe(review_data['df'], hide_index=True, width="stretch")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Discard", type="tertiary", width="stretch", key="discard_voice_btn"):
                st.session_state.pop('voice_review_data', None)
                st.rerun()
        with col2:
            if st.button("Confirm", type="primary", key="confirm_voice_attendence_btn", width="stretch"):
                try:
                    create_attendence(review_data['logs'])
                    st.toast("Attendance successfully recorded!", icon="✅")
                    st.session_state.pop('voice_review_data', None)
                    st.rerun()
                except Exception as e:
                    st.toast(icon="⚠️", body=f"Sync Failed: {str(e)}")  
                    st.rerun()