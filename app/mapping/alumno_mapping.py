from app.models.alumno import Alumno
from app.mapping.tipodocumento_mapping import TipoDocumentoMapping
from app.mapping.especialidad_mapping import EspecialidadMapping


class AlumnoMapping:
    """
    Clase para mapear datos JSON a objetos Alumno.
    Maneja dinámicamente los campos que vengan del servicio externo.
    """
    
    CAMPOS_CONOCIDOS = [
        "id", "apellido", "nombre", "nro_documento", 
        "tipo_documento_id", "fecha_nacimiento", "sexo",
        "nro_legajo", "fecha_ingreso"
    ]

    CAMPOS_ANIDADOS = ["tipo_documento", "especialidad"]
    
    @staticmethod
    def from_json(data: dict) -> Alumno:
        """
        Convierte datos JSON a un objeto Alumno.
        Mapea campos conocidos y guarda los desconocidos en datos_extra.
        
        Args:
            data: Diccionario con datos del alumno desde el servicio externo
            
        Returns:
            Instancia de Alumno
        """
        if not data:
            return Alumno()
        
        alumno = Alumno()

        for campo in AlumnoMapping.CAMPOS_CONOCIDOS:
            if campo in data:
                setattr(alumno, campo, data[campo])

        tipo_doc_data = data.get("tipo_documento")
        if tipo_doc_data:
            alumno.tipo_documento = TipoDocumentoMapping.from_json(tipo_doc_data)
        
        # Mapear especialidad si existe
        especialidad_data = data.get("especialidad")
        if especialidad_data:
            alumno.especialidad = EspecialidadMapping.from_json(especialidad_data)

        campos_procesados = (
            AlumnoMapping.CAMPOS_CONOCIDOS + 
            AlumnoMapping.CAMPOS_ANIDADOS
        )
        for key, value in data.items():
            if key not in campos_procesados:
                alumno.datos_extra[key] = value
        
        return alumno
    
    @staticmethod
    def from_json_list(data_list: list) -> list:
        """Convierte una lista JSON a lista de Alumnos."""
        if not data_list:
            return []
        return [AlumnoMapping.from_json(item) for item in data_list]