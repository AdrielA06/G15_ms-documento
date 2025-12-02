from dataclasses import dataclass, field
from app.models.tipodocumento import TipoDocumento
from app.models.especialidad import Especialidad


@dataclass(init=False, repr=True, eq=True)
class Alumno:

    id: int = 0
    apellido: str = ""
    nombre: str = ""
    nro_documento: str = ""
    tipo_documento_id: int = 0
    fecha_nacimiento: str = ""
    sexo: str = ""
    nro_legajo: int = 0
    fecha_ingreso: str = ""

    tipo_documento: TipoDocumento = None
    especialidad: Especialidad = None
    
    datos_extra: dict = field(default_factory=dict)
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.apellido}, {self.nombre}"
    
    @property
    def documento_completo(self) -> str:
        if self.tipo_documento:
            return f"{self.tipo_documento.nombre}: {self.nro_documento}"
        return self.nro_documento
    
    @property
    def especialidad_nombre(self) -> str:
        if self.especialidad:
            return self.especialidad.nombre
        return "Sin especialidad"
    
    @property
    def legajo_formateado(self) -> str:
        return str(self.nro_legajo)
    
    def get_campo(self, nombre_campo: str, default=""):
        if hasattr(self, nombre_campo):
            return getattr(self, nombre_campo, default)
        return self.datos_extra.get(nombre_campo, default)