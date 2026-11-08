
from flask import Flask
from flask_appbuilder import AppBuilder
from extensions import db

app = Flask(__name__)
app.config.from_object("config")

# Inicializar base de datos
db.init_app(app)

# Crear Flask-AppBuilder
appbuilder = AppBuilder()

with app.app_context():

    appbuilder.init_app(app, db.session)

    # Importar modelos antes de registrar vistas
    from app import models

    from app.views import (
        CarreraView,
        EstudianteView,
        DocenteView,
        MateriaView,
        InscripcionView,
        CalificacionView,
        ReportesView,
        AsistenteIAView
    )

    # Modulos academicos
    appbuilder.add_view(
        CarreraView, "Carreras",
        icon="fa-graduation-cap",
        category="Gestion academica"
    )

    appbuilder.add_view(
        EstudianteView, "Estudiantes",
        icon="fa-users",
        category="Gestion academica"
    )

    appbuilder.add_view(
        DocenteView, "Docentes",
        icon="fa-chalkboard-teacher",
        category="Gestion academica"
    )

    appbuilder.add_view(
        MateriaView, "Materias",
        icon="fa-book",
        category="Gestion academica"
    )

    appbuilder.add_view(
        InscripcionView, "Inscripciones",
        icon="fa-clipboard-list",
        category="Gestion academica"
    )

    appbuilder.add_view(
        CalificacionView, "Calificaciones",
        icon="fa-star",
        category="Gestion academica"
    )

    # Consultas y herramientas
    appbuilder.add_view(
        ReportesView, "Reportes",
        icon="fa-chart-bar",
        category="Consultas"
    )

    appbuilder.add_view(
        AsistenteIAView, "Asistente IA",
        icon="fa-robot",
        category="Consultas"
    )

