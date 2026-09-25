from src.database.db import check_teacher_exists, check_teacher, teacher_login

def register_teacher(teacher_name, teacher_username, teacher_pwd, teacher_cfm_pwd):
    if not teacher_name or not teacher_username or not teacher_pwd or not teacher_cfm_pwd:
        return False, "Please fill in all fields."
    if teacher_pwd != teacher_cfm_pwd:
        return False, "Passwords do not match."
    if check_teacher_exists(teacher_username):
        return False, "Username already exists."
    try:
        check_teacher(teacher_username, teacher_name, teacher_pwd)
        return True, "Welcome, " + teacher_username + "!"
    except Exception as e:
        return False, f"Error registering teacher: {str(e)}"

def login_teacher(teacher_username, teacher_pwd):
    if not teacher_username or not teacher_pwd:
        return False, "Please fill in all fields."
    teacher = teacher_login(teacher_username, teacher_pwd)
    if teacher:
        return True, "Welcome Back, " + teacher_username + "!"
    else:
        return False, "Invalid username or password."