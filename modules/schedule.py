# modules/schedule.py
import streamlit as st

def schedule_activity(member_id: int, activity_id: int, fecha: str, turno: str, monitor_id: int):
    """
    Agenda una actividad determinada para un miembro.
    """
    supabase = st.session_state.get("supabase_client")
    if not supabase:
        st.error("Cliente de Supabase no inicializado.") # Añadido control por si supabase no está inicializado
        return None

    data = {
        "member_id": member_id,
        "activity_id": activity_id,
        "fecha": fecha,
        "turno": turno,
        "monitor_id": monitor_id
    }
    try:
        response = supabase.table("schedule").insert(data).execute()
        return response
    except Exception as e:
        st.error(f"Error al agendar la actividad: {e}") # Captura excepciones más generales
        return None
