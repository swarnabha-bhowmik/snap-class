import streamlit as st
from src.database.db import (
    create_subject,
    get_teacher,
    is_student_enrolled,
    get_subject_by_code,
    enroll_student,
    get_student_subjects,
)

def check_subject(sub_id, sub_name, sub_section, teacher_username):
    if not sub_id or not sub_name or not sub_section:
        return False, "Please fill in all fields."
    teacher_id = get_teacher(teacher_username)
    try:
        create_subject(sub_id, sub_name, sub_section, teacher_id)
        return True, "Subject Created Successfully"
    except:
        return False, "Error Occured, Try again later"

def check_enroll(join_code, student_id=None):
    if not join_code or not join_code.strip():
        return False, "Please enter a subject code."

    if student_id is None:
        student_id = st.session_state.get('student_id')

    if not student_id:
        return False, "Student ID not found. Please log in again."

    subject = get_subject_by_code(join_code.strip())
    if not subject:
        return False, "Subject not found with the provided code."

    subject_id = subject.get("subject_id") or subject.get("id")
    if is_student_enrolled(student_id, subject_id):
        return False, f"You are already enrolled in {subject.get('name', 'this subject')}."

    try:
        enroll_student(student_id, subject_id)
        return True, f"Successfully enrolled in {subject.get('name', 'the subject')}!"
    except Exception:
        return False, "Error enrolling in subject. Please try again later."

def get_enrolled_subjects_for_student(student_id=None):
    if student_id is None:
        student_id = st.session_state.get('student_id')
    if not student_id:
        return []
    try:
        return get_student_subjects(student_id)
    except Exception:
        return []