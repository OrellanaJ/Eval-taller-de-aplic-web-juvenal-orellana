from flask_appbuilder import ModelView, BaseView, expose
from flask import request
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.security.decorators import has_access
from sqlalchemy import func
from extensions import db
from app.models import Carrera, Estudiante, Docente, Materia, Inscripcion, Calificacion
from app.ai_service import analizar_rendimiento

class CarreraView(ModelView):
    datamodel = SQLAInterface(Carrera)
    label_columns = {"duracion_semestres": "Duración (semestres)"}
    list_columns = ["nombre", "duracion_semestres", "activo"]
    show_columns = ["nombre", "descripcion", "duracion_semestres", "activo"]
    search_columns = ["nombre"]
    base_order = ("nombre", "asc")

class EstudianteView(ModelView):
    datamodel = SQLAInterface(Estudiante)
    list_columns = ["codigo", "nombres", "apellidos", "ci", "correo", "carrera", "estado"]
    show_columns = list_columns + ["telefono", "fecha_nacimiento", "fecha_ingreso"]
    search_columns = ["codigo", "nombres", "apellidos", "ci", "correo"]
    related_views = []

class DocenteView(ModelView):
    datamodel = SQLAInterface(Docente)
    list_columns = ["nombres", "apellidos", "correo", "especialidad", "activo"]
    show_columns = list_columns + ["ci", "telefono"]
    search_columns = ["nombres", "apellidos", "correo"]

class MateriaView(ModelView):
    datamodel = SQLAInterface(Materia)
    list_columns = ["codigo", "nombre", "carrera", "semestre", "docente", "carga_horaria"]
    show_columns = list_columns
    search_columns = ["codigo", "nombre"]

class InscripcionView(ModelView):
    datamodel = SQLAInterface(Inscripcion)
    list_columns = ["estudiante", "materia", "periodo", "fecha_inscripcion", "estado"]
    show_columns = list_columns
    search_columns = ["periodo", "estado"]

class CalificacionView(ModelView):
    datamodel = SQLAInterface(Calificacion)
    list_columns = ["inscripcion", "evaluacion", "nota", "fecha"]
    show_columns = list_columns + ["observacion"]
    search_columns = ["evaluacion", "observacion"]

class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "resumen"
    @expose("/resumen/")
    @has_access
    def resumen(self):
        total_estudiantes = db.session.query(func.count(Estudiante.id)).scalar() or 0
        total_materias = db.session.query(func.count(Materia.id)).scalar() or 0
        total_docentes = db.session.query(func.count(Docente.id)).scalar() or 0
        return self.render_template(
            "reportes/resumen.html",
            total_estudiantes=total_estudiantes,
            total_materias=total_materias,
            total_docentes=total_docentes
        )

    @expose("/rendimiento/")
    @has_access
    def rendimiento(self):
        filas = (db.session.query(
            Estudiante.codigo, Estudiante.nombres, Estudiante.apellidos,
            func.avg(Calificacion.nota).label("promedio"),
            func.count(Calificacion.id).label("evaluaciones")
        ).join(Inscripcion, Inscripcion.estudiante_id == Estudiante.id)
         .join(Calificacion, Calificacion.inscripcion_id == Inscripcion.id)
         .group_by(Estudiante.id).order_by(func.avg(Calificacion.nota).desc()).all())
        return self.render_template("reportes/rendimiento.html", filas=filas)

    @expose("/inscripciones/")
    @has_access
    def inscripciones(self):
        filas = (db.session.query(
            Materia.nombre, Inscripcion.periodo,
            func.count(Inscripcion.id).label("cantidad")
        ).join(Materia, Materia.id == Inscripcion.materia_id)
         .group_by(Materia.id, Inscripcion.periodo)
         .order_by(Inscripcion.periodo.desc(), Materia.nombre).all())
        return self.render_template("reportes/inscripciones.html", filas=filas)

class AsistenteIAView(BaseView):
    route_base = "/asistente-ia"
    default_view = "analizar"
    @expose("/", methods=["GET", "POST"])
    @has_access
    def analizar(self):
        resultado = None
        estudiante_id = None
        if request.method == "POST":
            estudiante_id = request.form.get("estudiante_id", type=int)
            estudiante = db.session.get(Estudiante, estudiante_id) if estudiante_id else None
            if estudiante:
                notas = (db.session.query(Calificacion.nota, Calificacion.evaluacion, Materia.nombre)
                    .join(Inscripcion, Calificacion.inscripcion_id == Inscripcion.id)
                    .join(Materia, Inscripcion.materia_id == Materia.id)
                    .filter(Inscripcion.estudiante_id == estudiante.id).all())
                resultado = analizar_rendimiento(estudiante, notas)
            else:
                resultado = "Seleccione un estudiante válido."
        estudiantes = Estudiante.query.order_by(Estudiante.apellidos).all()
        return self.render_template("asistente_ia.html", estudiantes=estudiantes,
                                    resultado=resultado, estudiante_id=estudiante_id)
