# streamlit_app.py
import streamlit as st
import datetime
from supabase import create_client
from modules import auth, members, schedule, reports

def init_supabase():
    # CREDENCIALES DE SUPABASE HARDCODEADAS (¡NO RECOMENDADO PARA PRODUCCIÓN!)
    SUPABASE_URL = "https://anqvjvjpcokkwspaecfc.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFucXZqdmpwY29ra3dzcGFlY2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1OTMyMDcsImV4cCI6MjA1NjE2OTIwN30.w4Y6sE8UyIA22pt5QAYQlcsWZceksF4AKF0zm7Jv7Lk"
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def login_page():
    print("**LOGIN_PAGE FUNCTION STARTED**") # LOG AÑADIDO AL INICIO DE login_page()
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Ingresar"):
        user = auth.login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.monitor = user
            st.success("Bienvenido " + user["username"])
            st.experimental_rerun()
        else:
            st.error("Credenciales incorrectas")
    print("**LOGIN_PAGE FUNCTION ENDED**") # LOG AÑADIDO AL FINAL DE login_page()


def register_member_page():
    st.title("Registrar Miembro")
    # ... (resto del código de register_member_page) ...

def schedule_activity_page():
    st.title("Agendar Actividad")
    # ... (resto del código de schedule_activity_page) ...

def report_page():
    st.title("Reportes de Actividades")
    # ... (resto del código de report_page) ...

def main():
    print("**MAIN FUNCTION STARTED**") # LOG AÑADIDO AL INICIO DE main()
    st.title("Gestión del Gimnasio")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "supabase_client" not in st.session_state:
        client = init_supabase()
        if not client:
            st.error("Error al inicializar Supabase. Revisa las credenciales en el código.") # Mensaje de error más claro
            return  # Sale de main() si no se inicializa Supabase
        st.session_state.supabase_client = client

    if not st.session_state.logged_in:
        login_page()
    else:
        menu_options = ["Registrar Miembro", "Agendar Actividad", "Reportes", "Cerrar Sesión"]
        menu = st.sidebar.radio("Navegación", options=menu_options)
        if menu == "Registrar Miembro":
            register_member_page()
        elif menu == "Agendar Actividad":
            schedule_activity_page()
        elif menu == "Reportes":
            report_page()
        elif menu == "Cerrar Sesión":
            st.session_state.logged_in = False
            st.experimental_rerun()
    print("**MAIN FUNCTION ENDED**") # LOG AÑADIDO AL FINAL DE main()


if __name__ == '__main__':
    main()
