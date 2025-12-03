from app.models.especialidad import Especialidad


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