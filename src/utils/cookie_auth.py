import datetime
import streamlit as st
import extra_streamlit_components as stx
import jwt

COOKIE_NAME = "snapclass_auth_token"
DEFAULT_SECRET = "snapclass_ai_attendance_jwt_secure_secret_key_2026_x99!"
JWT_ALGORITHM = "HS256"

def get_jwt_secret() -> str:
    """Retrieve secret key from st.secrets if configured, else fallback to stable default."""
    try:
        return st.secrets.get("AUTH_SECRET_KEY", DEFAULT_SECRET)
    except Exception:
        return DEFAULT_SECRET

def get_cookie_manager():
    """Initializes and returns the CookieManager component instance."""
    if "cookie_manager" not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager(key="snapclass_cookie_mgr")
    return st.session_state.cookie_manager

def create_auth_token(role: str, user_id, user_data: str, days: int = 30) -> str:
    """Creates a signed, time-limited JWT for persistent browser authentication."""
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "role": role,
        "user_id": str(user_id) if user_id is not None else None,
        "user_data": str(user_data),
        "iat": now,
        "exp": now + datetime.timedelta(days=days),
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)

def decode_auth_token(token: str) -> dict | None:
    """Decodes and cryptographically verifies the JWT auth token."""
    if not token:
        return None
    try:
        return jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

def save_auth_cookie(role: str, user_id, user_data: str, cookie_manager=None):
    """Encodes session data into a JWT and stores it in a browser cookie for 30 days."""
    cm = cookie_manager or get_cookie_manager()
    token = create_auth_token(role, user_id, user_data, days=30)
    expires = datetime.datetime.now() + datetime.timedelta(days=30)
    cm.set(
        COOKIE_NAME,
        token,
        key="set_auth_cookie",
        expires_at=expires,
        path="/",
    )

def clear_auth_cookie(cookie_manager=None):
    """Deletes the authentication cookie and marks the session as explicitly logged out."""
    cm = cookie_manager or get_cookie_manager()
    try:
        cm.delete(COOKIE_NAME, key="delete_auth_cookie")
    except Exception:
        pass
    st.session_state['logged_out'] = True

def restore_session_from_cookie(cookie_manager=None) -> bool:
    """
    Checks the browser cookie on page reload and restores the authenticated session.
    Returns True if an active session was successfully restored, False otherwise.
    """
    if st.session_state.get('logged_out'):
        return False

    if st.session_state.get('is_logged_in'):
        return True

    cm = cookie_manager or get_cookie_manager()

    # 1. First check native st.context.cookies (immediate upon browser reload)
    token = None
    try:
        if hasattr(st, "context") and hasattr(st.context, "cookies"):
            token = st.context.cookies.get(COOKIE_NAME)
    except Exception:
        token = None

    # 2. Fallback to CookieManager component
    if not token:
        try:
            token = cm.get(COOKIE_NAME)
        except Exception:
            token = None

    if not token:
        return False

    payload = decode_auth_token(token)
    if not payload:
        clear_auth_cookie(cm)
        return False

    role = payload.get("role")
    user_id = payload.get("user_id")
    user_data = payload.get("user_data")

    if role == "teacher":
        try:
            from src.database.db import check_teacher_exists
            if not check_teacher_exists(user_data):
                clear_auth_cookie(cm)
                return False
        except Exception:
            # If DB is temporarily unreachable, trust the signed token
            pass

        st.session_state['teacher_data'] = user_data
        st.session_state['user_role'] = "teacher"
        st.session_state['is_logged_in'] = True
        if st.session_state.get('login_type') is None or st.session_state.get('login_type') == "teacher":
            st.session_state['login_type'] = "teacher_dashboard"
        return True

    elif role == "student":
        student_id_val = user_id
        student_name_val = user_data
        try:
            from src.database.db import get_student_by_id, get_all_students
            student = None
            if user_id:
                student = get_student_by_id(user_id)
            if not student:
                all_students = get_all_students() or []
                if user_id:
                    student = next((s for s in all_students if str(s.get('student_id')) == str(user_id)), None)
                if not student and user_data:
                    student = next((s for s in all_students if s.get('name') == user_data), None)

            if student:
                student_id_val = student.get('student_id')
                student_name_val = student.get('name', user_data)
        except Exception:
            pass

        st.session_state['student_id'] = student_id_val
        st.session_state['student_data'] = student_name_val
        st.session_state.user_role = "student"
        st.session_state['is_logged_in'] = True
        student_auth_views = {"student", "student_face_login", "student_screen_signup"}
        if st.session_state.get('login_type') is None or st.session_state.get('login_type') in student_auth_views:
            st.session_state['login_type'] = "student_dashboard"
        return True

    return False
