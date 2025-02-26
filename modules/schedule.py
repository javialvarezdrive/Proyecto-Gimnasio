import streamlit as st

def schedule_activity(member_id: int, activity_id: int, fecha: str, turno: str, monitor_id: int):
    """
    Agenda una actividad para un miembro, registrando la fecha, turno, y el monitor que agendó.
    """
    supabase = st.session_state.supabase_client
    data = {
        "member_id": member_id,
        "activity_id": activity_id,
        "fecha": fecha,
        "turno": turno,
        "monitor_id": monitor_id
    }
    response = supabase.table("schedule").insert(data).execute()
    return response
