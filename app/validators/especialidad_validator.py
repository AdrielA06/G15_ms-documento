from app.models.especialidad import Especialidad


def validar_especialidad_completa(especialidad: Especialidad) -> tuple:
    errores = []
    
    valida_modelo, errores_modelo = especialidad.validar()
    
    if not valida_modelo:
        errores.extend(errores_modelo)
    
    return (len(errores) == 0, errores)


def validar_especialidad_para_certificado(especialidad: Especialidad) -> tuple:
    errores = []
    
    valida_modelo, errores_modelo = especialidad.validar()
    
    if not valida_modelo:
        errores.extend(errores_modelo)
    
    if not especialidad.titulo or not especialidad.titulo.strip():
        errores.append("La especialidad debe tener un título definido para el certificado")
    
    return (len(errores) == 0, errores)