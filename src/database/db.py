from src.database.config import supabase
import bcrypt
import numpy as np

def hash_pass(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_pass(password, hashed_pwd):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pwd.encode('utf-8'))

def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def check_teacher(username, name, password):
    data = {"username": username, "name": name, "password": hash_pass(password)}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def get_teacher(username):
    response = supabase.table("teachers").select("teacher_id").eq("username", username).execute()
    if response.data:
        return response.data[0]["teacher_id"]
    return None

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data

def student_login(email, password):
    response = supabase.table("students").select("*").eq("email", email).execute()
    if response.data:
        student = response.data[0]
        if check_pass(password, student["password"]):
            return student
    return None

def check_student_exists(email, face_embedding, voice_embedding):
    response = supabase.table("students").select("email, face_embedding, voice_embedding").execute()
    if not response.data:
        return False
    if email and any(student.get("email") == email for student in response.data):
        return True

    for student in response.data:
        stored_face = student.get("face_embedding")
        if face_embedding is not None and stored_face is not None:
            face_distance = np.linalg.norm(
                np.asarray(stored_face) - np.asarray(face_embedding)
            )
            if face_distance <= 0.6:
                return True

        stored_voice = student.get("voice_embedding")
        if voice_embedding is not None and stored_voice is not None:
            voice_similarity = np.dot(
                np.asarray(voice_embedding), np.asarray(stored_voice)
            )
            if voice_similarity >= 0.65:
                return True

    return False

def create_student(name, email, pwd, face_embedding, voice_embedding):
    data = {"name": name, "email": email, "password": hash_pass(pwd), "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_subject(sub_id, sub_name, sub_section, teacher_id):
    data = {"code": sub_id, "name": sub_name, "section": sub_section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_subjects(teacher_username):
    teacher_id = get_teacher(teacher_username)
    response = supabase.table("subjects").select("*, subject_student(count), attendance_logs(timestamps)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_student", [{}])[0].get('count', 0) if sub.get('subject_student') else 0
        attendence = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamps'] for log in attendence if 'timestamps' in log))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects

def get_subject_by_code(code):
    response = supabase.table("subjects").select("*").eq("code", code).execute()
    if response.data:
        return response.data[0]
    return None

def is_student_enrolled(student_id, subject_id):
    response = (
        supabase.table("subject_student")
        .select("*")
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return len(response.data) > 0

def enroll_student(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    try:
        response = supabase.table("subject_student").insert(data).execute()
        return response.data
    except:
        return None

def unenroll_student(student_id, subject_id):
    response = (
        supabase.table("subject_student")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data

def get_student_subjects(student_id):
    response = (
        supabase.table("subject_student")
        .select("subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    if response.data:
        return [item["subjects"] for item in response.data if item.get("subjects")]
    return []

def get_student_attendance(student_id):
    try:
        response = (
            supabase.table("attendance_logs")
            .select("*")
            .eq("student_id", student_id)
            .execute()
        )
        return response.data or []
    except Exception:
        return []

def get_subject_attendance_sessions(subject_id):
    try:
        response = (
            supabase.table("attendance_logs")
            .select("timestamps")
            .eq("subject_id", subject_id)
            .execute()
        )
        if response.data:
            return len(set(item["timestamps"] for item in response.data if "timestamps" in item))
        return 0
    except Exception:
        return 0

def create_attendence(logs):
    res = supabase.table('attendance_logs').insert(logs).execute()
    return res.data

def attendence_logs(teacher_id):
    res = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return res.data