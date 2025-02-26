import streamlit as st

def register_member(nip: str, nombre: str, apellidos: str, seccion: str, grupo: str):
    """
    Registra un miembro nuevo en la base de datos.
    """
    supabase = st.session_state.get("supabase_client")
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
    response = supabase.table("gym_members").insert(data).execute()
    return response
