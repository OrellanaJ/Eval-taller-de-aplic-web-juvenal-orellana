import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "CLAVE")
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost/gestion_estudiantes?charset=utf8mb4"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
APP_NAME = "Sistema de Gestión de Estudiantes"
APP_THEME = "cosmo"
