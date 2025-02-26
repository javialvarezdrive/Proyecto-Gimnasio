import streamlit as st
from supabase import create_client, Client

def login_user(username: str, password: str):
    """
    Valida las credenciales del monitor consultando la tabla "monitors" en Supabase.
    """
    # Usa el cliente de Supabase almacenado en session_state
    supabase: Client = st.session_state.get("supabase_client")
    if supabase is None:
        SUPABASE_URL = st.secrets["SUPABASE_URL"]
        SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        st.session_state.supabase_client = supabase

    response = supabase.table("monitors") \
                       .select("*") \
                       .eq("username", username) \
                       .eq("password", password) \
                       .execute()
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None
