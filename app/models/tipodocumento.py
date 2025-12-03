from dataclasses import dataclass, field

@dataclass(init=False, repr=True, eq=True)
class TipoDocumento():
    
    id: int = 0
    sigla: str = ""
    nombre: str = ""
    descripcion: str = ""
    
    datos_extra: dict = field(default_factory=dict)
    
    @property
    def sigla_nombre(self) -> str:
        return f"{self.sigla} - {self.nombre}"
    
    def get_campo(self, nombre_campo: str, default=""):
        if hasattr(self, nombre_campo):
            return getattr(self, nombre_campo, default)
        return self.datos_extra.get(nombre_campo, default)
    
    def set_campo_extra(self, nombre_campo: str, valor):
        self.datos_extra[nombre_campo] = valor
    
    def validar(self) -> tuple:
        errores = []
        
        if not self.sigla or not self.sigla.strip():
            errores.append("La sigla es obligatoria.")
        
        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre es obligatorio.")
        
        if len(self.sigla) > 10:
            errores.append("La sigla no puede tener más de 10 caracteres.")
        
        return (len(errores) == 0, errores)
    
    def es_valido(self) -> bool:
        valido, _ = self.validar()
        return valido
    
    def __str__(self) -> str:
        return f"TipoDocumento({self.id}): {self.sigla_nombre}"