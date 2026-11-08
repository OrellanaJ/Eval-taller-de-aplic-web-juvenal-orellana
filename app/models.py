from datetime import date
from extensions import db

class Carrera(db.Model):
    __tablename__ = "carreras"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    duracion_semestres = db.Column(db.Integer, default=8)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    estudiantes = db.relationship("Estudiante", back_populates="carrera")
    materias = db.relationship("Materia", back_populates="carrera")
    def __repr__(self): return self.nombre

class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(30), unique=True)
    correo = db.Column(db.String(150), unique=True)
    telefono = db.Column(db.String(30))
    fecha_nacimiento = db.Column(db.Date)
    fecha_ingreso = db.Column(db.Date, default=date.today)
    estado = db.Column(db.String(20), default="Activo", nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey("carreras.id"), nullable=False)
    carrera = db.relationship("Carrera", back_populates="estudiantes")
    inscripciones = db.relationship("Inscripcion", back_populates="estudiante", cascade="all, delete-orphan")
    def __repr__(self): return f"{self.codigo} - {self.apellidos}, {self.nombres}"

class Docente(db.Model):
    __tablename__ = "docentes"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    ci = db.Column(db.String(30), unique=True)
    correo = db.Column(db.String(150), unique=True)
    especialidad = db.Column(db.String(120))
    telefono = db.Column(db.String(30))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    materias = db.relationship("Materia", back_populates="docente")
    def __repr__(self): return f"{self.apellidos}, {self.nombres}"

class Materia(db.Model):
    __tablename__ = "materias"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)
    nombre = db.Column(db.String(120), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)
    carga_horaria = db.Column(db.Integer, default=64)
    carrera_id = db.Column(db.Integer, db.ForeignKey("carreras.id"), nullable=False)
    docente_id = db.Column(db.Integer, db.ForeignKey("docentes.id"))
    carrera = db.relationship("Carrera", back_populates="materias")
    docente = db.relationship("Docente", back_populates="materias")
    inscripciones = db.relationship("Inscripcion", back_populates="materia")
    def __repr__(self): return self.nombre

class Inscripcion(db.Model):
    __tablename__ = "inscripciones"
    id = db.Column(db.Integer, primary_key=True)
    fecha_inscripcion = db.Column(db.Date, default=date.today, nullable=False)
    periodo = db.Column(db.String(20), nullable=False)  # Ej.: 2026-2
    estado = db.Column(db.String(20), default="Regular", nullable=False)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("estudiantes.id"), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("materias.id"), nullable=False)
    estudiante = db.relationship("Estudiante", back_populates="inscripciones")
    materia = db.relationship("Materia", back_populates="inscripciones")
    calificaciones = db.relationship("Calificacion", back_populates="inscripcion", cascade="all, delete-orphan")
    __table_args__ = (db.UniqueConstraint("estudiante_id", "materia_id", "periodo", name="uq_inscripcion_periodo"),)
    def __repr__(self): return f"{self.estudiante} / {self.materia} ({self.periodo})"

class Calificacion(db.Model):
    __tablename__ = "calificaciones"
    id = db.Column(db.Integer, primary_key=True)
    evaluacion = db.Column(db.String(80), nullable=False)
    nota = db.Column(db.Numeric(5, 2), nullable=False)
    fecha = db.Column(db.Date, default=date.today, nullable=False)
    observacion = db.Column(db.Text)
    inscripcion_id = db.Column(db.Integer, db.ForeignKey("inscripciones.id"), nullable=False)
    inscripcion = db.relationship("Inscripcion", back_populates="calificaciones")
    def __repr__(self): return f"{self.evaluacion}: {self.nota}"
