# auth.py
import bcrypt
import streamlit as st
from supabase import create_client

def init_supabase():
    # Reemplaza con tus credenciales de Supabase
    SUPABASE_URL = "TU_SUPABASE_URL"
    SUPABASE_KEY = "TU_SUPABASE_KEY"
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

def login_user(username, password):
    response = supabase.table('monitors').select('*').eq('username', username).execute()
    if response.error:
        st.error(f"Error en la consulta: {response.error.message}")
        return None
    if not response.data:
        st.warning("Usuario no encontrado.")
        return None

    user = response.data[0]
    hashed_password = user['password']

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        return user  # Inicio de sesión exitoso
    else:
        st.warning("Contraseña incorrecta.")
        return None

def register_user(username, password, nombre, apellidos, email, rol='usuario'):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {
        'username': username,
        'password': hashed_password,
        'nombre': nombre,
        'apellidos': apellidos,
        'email': email,
        'rol': rol
    }
    response = supabase.table('monitors').insert(user_data).execute()
    if response.error:
        st.error(f"Error al registrar usuario: {response.error.message}")
        return False
    else:
        st.success(f"Usuario '{username}' registrado exitosamente.")
        return True
