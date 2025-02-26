# modules/__init__.py
from .auth import login_user, register_user  # Añadido register_user para consistencia, aunque no se use en el código principal dado
from .members import register_member
from .schedule import schedule_activity
from .reports import generate_report
