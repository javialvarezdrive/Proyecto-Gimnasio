# modules/members.py
import streamlit as st

def register_member(nip: str, nombre: str, apellidos: str, seccion: str, grupo: str):
    """
    Registra un miembro nuevo en la base de datos.
    """
    supabase = st.session_state.get("supabase_client")
    if not supabase:
        st.error("Cliente de Supabase no inicializado.") # Añadido control por si supabase no está inicializado
        return None
    try:
        nip_int = int(nip)
    except ValueError:
        st.error("El NIP debe ser numérico.")
        return None

    data = {
        "nip": nip_int,
        "nombre": nombre,
        "apellidos": apellidos,
        "seccion": seccion,
        "grupo": grupo
    }
    try:
        response = supabase.table("gym_members").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Error al registrar miembro: {e}") # Captura excepciones más generales
        return None
