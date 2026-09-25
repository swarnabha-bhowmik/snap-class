from src.database.db import check_student_exists, create_student, student_login
from src.pipelines.face_pipeline import get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

def register_student(student_name, student_email, student_pwd, student_cfm_pwd, img, audio):
    if not student_name or not student_email or not student_pwd or not student_cfm_pwd:
        return False, None, "Please fill in all the required fields."
    if student_pwd != student_cfm_pwd:
        return False, None, "Passwords do not match."
    if img is None:
        return False, None, "Please capture a face photo before signing up."

    encodings = get_face_embeddings(img)
    if not encodings:
        return False, None, "No face detected in the photo. Please take a clear picture."
    face_emb = encodings[0].tolist()

    voice_emb = None
    if audio:
        try:
            voice_emb = get_voice_embedding(audio.read())
        except Exception:
            voice_emb = None

    if check_student_exists(student_email, face_emb, voice_emb):
        return False, None, "Student already exists"
    try:
        created = create_student(student_name, student_email, student_pwd, face_emb, voice_emb)
        student_id = None
        if created and len(created) > 0:
            student_id = created[0].get("student_id")
        if not student_id:
            logged_in = student_login(student_email, student_pwd)
            if logged_in:
                student_id = logged_in.get("student_id")
        train_classifier()
        return True, student_id, f"Welcome, {student_name}!"
    except Exception:
        return False, None, "Error Registering Student"

def login_student(student_email, student_pwd):
    if not student_email or not student_pwd:
        return False, None, "Please fill in all the required fields."
    try:
        student = student_login(student_email, student_pwd)
        if student:
            name = student.get('name', 'Student')
            return True, student, f"Welcome Back, {name}!"
        else:
            return False, None, "Invalid email id or password"
    except Exception:
        return False, None, "Error logging in. Please check your credentials and try again."