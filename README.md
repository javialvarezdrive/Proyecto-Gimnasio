# Proyecto-Gimnasio

Este proyecto es una webapp desarrollada con Streamlit y Supabase para la gestión de un gimnasio.  
La aplicación permite:
- Autenticación de monitores.
- Registrar miembros del gimnasio.
- Agendar actividades (Defensa Personal, Acondicionamiento Físico, etc.).
- Generar reportes interactivos basados en las actividades agendadas.

## Estructura del Proyecto

- .streamlit/  
  Contiene el archivo secrets.toml con variables sensibles.

- assets/  
  Recursos estáticos (imágenes, logos, etc.).

- data/  
  Script SQL para crear y poblar la base de datos en Supabase.

- modules/  
  Módulos con las funcionalidades de autenticación, manejo de miembros, agendamiento y reportes.

- streamlit_app.py  
  Archivo principal que orquesta la aplicación.

- requirements.txt  
  Lista de dependencias.

## Instrucciones

1. Configurar el archivo .streamlit/secrets.toml con tu URL y KEY de Supabase.
2. Ejecutar el script SQL (data/setup_db.sql) para crear las tablas en Supabase.
3. Instalar las dependencias:
   pip install -r requirements.txt
4. Ejecutar la aplicación:
   streamlit run streamlit_app.py
