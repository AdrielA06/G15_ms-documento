from app.models.alumno import Alumno
from app.models.tipodocumento import TipoDocumento
from app.models.especialidad import Especialidad

def map_to_alumno(data) -> Alumno:
    alumno = Alumno()
    
    alumno.id = data.get("id", 0)
    alumno.apellido = data.get("apellido", "")
    alumno.nombre = data.get("nombre", "")
    alumno.nro_documento = data.get("nro_documento", "")
    alumno.tipo_documento_id = data.get("tipo_documento_id", 0)
    alumno.fecha_nacimiento = data.get("fecha_nacimiento", "")
    alumno.sexo = data.get("sexo", "")
    alumno.nro_legajo = data.get("nro_legajo", 0)
    alumno.fecha_ingreso = data.get("fecha_ingreso", "")
    
    if "tipo_documento" in data and data["tipo_documento"]:
        alumno.tipo_documento = map_to_tipo_documento(data["tipo_documento"])
    
    if "especialidad" in data and data["especialidad"]:
        alumno.especialidad = map_to_especialidad(data["especialidad"])
    
    if "datos_extra" in data:
        alumno.datos_extra = data["datos_extra"]
    
    return alumno

def map_to_tipo_documento(data) -> TipoDocumento:
    tipo = TipoDocumento()
    
    tipo.id = data.get("id", 0)
    tipo.sigla = data.get("sigla", "")
    tipo.nombre = data.get("nombre", "")
    tipo.descripcion = data.get("descripcion", "")
    
    if "datos_extra" in data:
        tipo.datos_extra = data["datos_extra"]
    
    return tipo

def map_to_especialidad(data) -> Especialidad:
    especialidad = Especialidad()
    
    especialidad.id = data.get("id", 0)
    especialidad.codigo = data.get("codigo", "")
    especialidad.nombre = data.get("nombre", "")
    especialidad.titulo = data.get("titulo", "")
    especialidad.duracion_anios = data.get("duracion_anios", 0)
    especialidad.plan_estudio = data.get("plan_estudio", "")
    especialidad.descripcion = data.get("descripcion", "")
    
    if "datos_extra" in data:
        especialidad.datos_extra = data["datos_extra"]
    
    return especialidad


class AlumnoMapping:
    """Clase wrapper para mapear datos de alumno."""
    
    def load(self, data) -> Alumno:
        """Mapea un diccionario a un objeto Alumno."""
        return map_to_alumno(data)