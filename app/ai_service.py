import os
from statistics import mean

def analizar_rendimiento(estudiante, notas):
    """Usa Gemini  API key; , ofrece un análisis local básico."""
    valores = [float(n.nota) for n in notas]
    if not valores:
        return "Este estudiante todavía no tiene calificaciones registradas. Registre evaluaciones para generar un análisis."

    promedio = round(mean(valores), 2)
    detalle = "\n".join(
        f"- {materia}: {evaluacion} = {float(nota):.2f}"
        for nota, evaluacion, materia in notas
    )
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = (
                "Actúa como orientador académico. Analiza estos datos sin inventar información. "
                "Explica fortalezas, posibles dificultades y tres recomendaciones concretas. "
                "No etiquetes ni diagnostiques al estudiante. "
                f"Estudiante: {estudiante.nombres} {estudiante.apellidos}. "
                f"Promedio calculado: {promedio}. Notas:\n{detalle}"
            )
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
                contents=prompt
            )
            return response.text or "La IA no devolvió contenido. Intente nuevamente."
        except Exception as exc:
            return (f"No se pudo conectar con el servicio de IA ({type(exc).__name__}). "
                    f"Análisis local: promedio {promedio}/100. "
                    + ("Rendimiento satisfactorio." if promedio >= 70 else "Se recomienda tutoría y seguimiento académico."))
    estado = "satisfactorio" if promedio >= 70 else "que requiere seguimiento"
    return (
        f"Análisis automático local para {estudiante.nombres} {estudiante.apellidos}:\n"
        f"Promedio general: {promedio}/100. El rendimiento actual es {estado}.\n"
        "Recomendaciones: 1) revisar las materias con notas más bajas; "
        "2) establecer un horario semanal de estudio; "
        "3) coordinar tutorías con el docente y volver a evaluar el progreso.\n"
        "Nota: configure GEMINI_API_KEY para habilitar el análisis generativo."
    )
