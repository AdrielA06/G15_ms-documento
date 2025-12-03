from dataclasses import dataclass, field
from datetime import datetime
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
        return f"LEG-{str(self.nro_legajo).zfill(5)}"
    
    def edad(self) -> int:
        if not self.fecha_nacimiento:
            return 0
        try:
            fecha_nac = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
            hoy = datetime.today()
            edad = hoy.year - fecha_nac.year 
            
            if(hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1
            return edad
        except ValueError:
            return 0
    
    def get_campo(self, nombre_campo: str, default=""):
        if hasattr(self, nombre_campo):
            return getattr(self, nombre_campo, default)
        return self.datos_extra.get(nombre_campo, default)
    
    def set_campo_extra(self, nombre_campo: str, valor):
        self.datos_extra[nombre_campo] = valor
    
    def validar(self) -> tuple:
        errores = []
        
        if not self.apellido or not self.apellido.strip():
            errores.append("El apellido es obligatorio.")
        
        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre es obligatorio.")
        
        if not self.nro_documento or not self.nro_documento.strip():
            errores.append("El número de documento es obligatorio.")
        elif not self.nro_documento.isdigit():
            errores.append("El número de documento debe contener solo dígitos.")
        
        if self.tipo_documento_id <= 0:
            errores.append("Debe seleccionarse un tipo de documento válido.")
        
        if self.nro_legajo <= 0:
            errores.append("El número de legajo debe ser un entero positivo.")
        
        if self.fecha_nacimiento:
            try:
                fecha_nac = datetime.strptime(self.fecha_nacimiento, "%Y-%m-%d")
                if fecha_nac > datetime.now():
                    errores.append("La fecha de nacimiento no puede ser futura.")
            except ValueError:
                errores.append("La fecha de nacimiento no tiene un formato válido (YYYY-MM-DD).")
        else:
            errores.append("La fecha de nacimiento es obligatoria.")
        
        if self.fecha_ingreso:
            try:
                fecha_ing = datetime.strptime(self.fecha_ingreso, "%Y-%m-%d")
                if fecha_ing > datetime.now():
                    errores.append("La fecha de ingreso no puede ser futura.")
            except ValueError:
                errores.append("La fecha de ingreso no tiene un formato válido (YYYY-MM-DD).")
        else:
            errores.append("La fecha de ingreso es obligatoria.")
        
        if self.sexo and self.sexo.upper() not in ['M', 'F', 'O']:
            errores.append("El sexo debe ser 'M', 'F' o 'O' si se especifica.")
        
        return (len(errores) == 0, errores)
    
    def es_valido(self) -> bool:
        valido, _ = self.validar()
        return valido
    
    def __str__(self) -> str:
        return f"Alumno({self.id}): {self.nombre_completo} - {self.documento_completo}"