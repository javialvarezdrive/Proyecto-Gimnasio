import streamlit as st
from supabase import create_client

def login_user(username: str, password: str):
    """
    Valida las credenciales del monitor usando Supabase.
    """
    supabase = st.session_state.get("supabase_client")
    if not supabase:
        st.error("No se ha inicializado el cliente de Supabase.")
        return None

    response = supabase.table("monitors")\
                       .select("*")\
                       .eq("username", username)\
                       .eq("password", password)\
                       .execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None
