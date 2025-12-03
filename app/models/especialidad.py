from dataclasses import dataclass, field
@dataclass(init=False, repr=True, eq=True)
class Especialidad():
    id: int = 0
    codigo: str = ""
    nombre: str = ""
    titulo: str = ""
    duracion_anios: int = 0
    plan_estudio: str = ""
    descripcion: str = ""
    
    datos_extra: dict = field(default_factory=dict)
    
    @property
    def codigo_nombre(self) -> str:
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def duracion_completa(self) -> str:
        anio_plural = "años" if self.duracion_anios != 1 else "año"
        return f"{self.duracion_anios} {anio_plural}"
    
    def get_campo(self, nombre_campo: str, default=""):
        if hasattr(self, nombre_campo):
            return getattr(self, nombre_campo, default)
        return self.datos_extra.get(nombre_campo, default)
    
    def set_campo_extra(self, nombre_campo: str, valor):
        self.datos_extra[nombre_campo] = valor
    
    def validar(self) -> tuple:
        errores = []
        
        if not self.codigo or not self.codigo.strip():
            errores.append("El código es obligatorio.")
        
        if not self.nombre or not self.nombre.strip():
            errores.append("El nombre es obligatorio.")
        
        if not self.titulo or not self.titulo.strip():
            errores.append("El título es obligatorio.")
        
        if self.duracion_anios <= 0:
            errores.append("La duración debe ser mayor a 0 años.")
        
        if not self.plan_estudio or not self.plan_estudio.strip():
            errores.append("El plan de estudio es obligatorio.")
        
        return (len(errores) == 0, errores)
    
    def es_valida(self) -> bool:
        valida, _ = self.validar()
        return valida
    
    def __str__(self) -> str:
        return f"Especialidad({self.id}): {self.codigo_nombre}"