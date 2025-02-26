# modules/auth.py
import bcrypt
import streamlit as st
from supabase import create_client

def init_supabase():
    # CREDENCIALES DE SUPABASE HARDCODEADAS (¡NO RECOMENDADO PARA PRODUCCIÓN!)
    SUPABASE_URL = "https://anqvjvjpcokkwspaecfc.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFucXZqdmpwY29ra3dzcGFlY2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1OTMyMDcsImV4cCI6MjA1NjE2OTIwN30.w4Y6sE8UyIA22pt5QAYQlcsWZceksF4AKF0zm7Jv7Lk"
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

def login_user(username, password):
    try:
        response = supabase.table('monitors').select('*').eq('username', username).execute()
        # Manejo de errores revisado según la documentación actual de supabase-py
        if response.error:
            st.error(f"Error en la consulta de login: {response.error.message}")
            return None

        data = response.data

        if not data:
            st.warning("Usuario no encontrado.")
            return None

        user = data[0]
        hashed_password_db = user['password']

        if hashed_password_db and bcrypt.checkpw(password.encode('utf-8'), hashed_password_db.encode('utf-8')):
            return user  # Inicio de sesión exitoso
        else:
            st.warning("Contraseña incorrecta.")
            return None
    except Exception as e:
        st.error(f"Error inesperado durante el login: {e}")
        return None

def register_user(username, password, nombre, apellidos, email, rol='monitor'): # Rol cambiado a 'monitor' para consistencia con 'monitors' table
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_data = {
            'username': username,
            'password': hashed_password,
            'nombre': nombre,
            'apellidos': apellidos,
            'email': email,
            'rol': rol # Usando el rol pasado como argumento
        }
        response = supabase.table('monitors').insert(user_data).execute()
        if response.error:
            st.error(f"Error al registrar usuario: {response.error.message}")
            return False
        else:
            st.success(f"Usuario '{username}' registrado exitosamente.")
            return True
    except Exception as e:
        st.error(f"Error inesperado durante el registro de usuario: {e}")
        return False
