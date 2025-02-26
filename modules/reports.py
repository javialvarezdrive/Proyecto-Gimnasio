# modules/reports.py
import streamlit as st
import pandas as pd
import plotly.express as px

def generate_report(start_date, end_date):
    """
    Genera un reporte gráfico de las actividades agendadas,
    filtrando entre start_date y end_date.
    """
    supabase = st.session_state.get("supabase_client")
    if not supabase:
        st.error("Cliente de Supabase no inicializado.") # Añadido control por si supabase no está inicializado
        return None, None

    try:
        response = supabase.table("schedule")\
                           .select("*, gym_members(*), activities(*)")\
                           .gte("fecha", start_date.isoformat())\
                           .lte("fecha", end_date.isoformat())\
                           .execute()
        if response.error:
            st.error("Error al recuperar datos del reporte: " + response.error.message)
            return None, None
        data = response.data
        if not data:
            st.info("No hay datos en el rango de fechas seleccionado para el reporte.")
            return None, None

        df = pd.DataFrame(data)
        if "activities" in df.columns:
            df["actividad"] = df["activities"].apply(
                lambda x: x.get("nombre") if isinstance(x, dict) else "Desconocida"
            )
            conteo = df.groupby("actividad").size().reset_index(name="conteo")
            fig = px.bar(conteo, x="actividad", y="conteo", title="Cantidad de Actividades Agendadas") # Título más descriptivo
            return fig, df
        else:
            st.warning("No se encontró información de actividades en los datos recuperados.")
            return None, df
    except Exception as e:
        st.error(f"Error inesperado al generar el reporte: {e}") # Captura excepciones más generales
        return None, None
