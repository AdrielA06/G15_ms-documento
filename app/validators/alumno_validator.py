from app.models.alumno import Alumno


def validar_alumno_completo(alumno: Alumno) -> tuple:
    errores = []
    
    valido_modelo, errores_modelo = alumno.validar()
    
    if not valido_modelo:
        errores.extend(errores_modelo)
    
    return (len(errores) == 0, errores)


def validar_alumno_para_certificado(alumno: Alumno) -> tuple:
    errores = []
    
    valido_modelo, errores_modelo = alumno.validar()
    
    if not valido_modelo:
        errores.extend(errores_modelo)
    
    if alumno.especialidad is None:
        errores.append("El alumno debe tener una especialidad asignada para generar el certificado")
    
    if alumno.tipo_documento is None:
        errores.append("El alumno debe tener un tipo de documento asignado")
    
    return (len(errores) == 0, errores)


def validar_alumno_para_ficha(alumno: Alumno) -> tuple:
    errores = []
    
    valido_modelo, errores_modelo = alumno.validar()
    
    if not valido_modelo:
        errores.extend(errores_modelo)
    
    if alumno.tipo_documento is None:
        errores.append("El alumno debe tener un tipo de documento asignado para generar la ficha")
    
    return (len(errores) == 0, errores)