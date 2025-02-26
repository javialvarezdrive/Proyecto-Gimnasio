import streamlit as st
import datetime
from supabase import create_client
from modules import auth, members, schedule, reports

def init_supabase():
    # Reemplaza con tus credenciales de Supabase
    SUPABASE_URL = "https://anqvjvjpcokkwspaecfc.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFucXZqdmpwY29ra3dzcGFlY2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1OTMyMDcsImV4cCI6MjA1NjE2OTIwN30.w4Y6sE8UyIA22pt5QAYQlcsWZceksF4AKF0zm7Jv7Lk"
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def login_page():
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

def register_member_page():
    st.title("Registrar Miembro")
    with st.form("form_registro_member"):
        nip = st.text_input("NIP")
        nombre = st.text_input("Nombre")
        apellidos = st.text_input("Apellidos")
        seccion = st.selectbox("Sección", options=["SETRA", "Motorista", "GOA", "Patrullas"])
        grupo = st.selectbox("Grupo", options=["G-1", "G-2", "G-3"])
        submitted = st.form_submit_button("Registrar")
    if submitted:
        response = members.register_member(nip, nombre, apellidos, seccion, grupo)
        if response and response.status_code in (200, 201):
            st.success("Miembro registrado correctamente.")
        else:
            st.error("Error al registrar el miembro.")

def schedule_activity_page():
    st.title("Agendar Actividad")
    fecha = st.date_input("Seleccione la fecha", value=datetime.date.today())
    turno = st.selectbox("Turno", options=["Mañana", "Tarde", "Noche"])
    supabase = st.session_state.get("supabase_client")
    if not supabase:
        st.error("Supabase no está inicializado.")
        return

    # Lista de miembros
    member_resp = supabase.table("gym_members").select("*").execute()
    if member_resp.error:
        st.error("Error al obtener los miembros: " + member_resp.error.message)
        return
    members_data = member_resp.data
    member_options = {f"{m['nombre']} {m['apellidos']} - {m['nip']}": m["id"] for m in members_data}
    selected_member = st.selectbox("Seleccione Miembro", options=list(member_options.keys()))

    # Lista de actividades
    act_resp = supabase.table("activities").select("*").execute()
    if act_resp.error:
        st.error("Error al obtener las actividades: " + act_resp.error.message)
        return
    activities_data = act_resp.data
    activity_options = {act["nombre"]: act["id"] for act in activities_data}
    selected_activity = st.selectbox("Seleccione Actividad", options=list(activity_options.keys()))

    if st.button("Agendar Actividad"):
        result = schedule.schedule_activity(
            member_id=member_options[selected_member],
            activity_id=activity_options[selected_activity],
            fecha=fecha.isoformat(),
            turno=turno,
            monitor_id=st.session_state.monitor["id"]
        )
        if result and result.status_code in (200, 201):
            st.success("Actividad agendada con éxito.")
        else:
            st.error("Error al agendar la actividad.")

def report_page():
    st.title("Reportes de Actividades")
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Fecha inicio", value=datetime.date.today() - datetime.timedelta(days=30))
    end_date = col2.date_input("Fecha fin", value=datetime.date.today())
    if st.button("Generar Reporte"):
        fig, df = reports.generate_report(start_date, end_date)
        if fig:
            st.plotly_chart(fig)
        if df is not None:
            st.dataframe(df)

def main():
    st.title("Gestión del Gimnasio")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "supabase_client" not in st.session_state:
        client = init_supabase()
        if not client:
            return  # Se mostrará el error
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

if __name__ == '__main__':
    main()
