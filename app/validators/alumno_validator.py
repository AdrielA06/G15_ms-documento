from app.models.alumno import Alumno


def _validar_base(alumno: Alumno) -> list:
    """
    Valida los datos base del alumno.
    
    Args:
        alumno: Objeto Alumno a validar
        
    Returns:
        Lista de errores encontrados
    """
    valido_modelo, errores_modelo = alumno.validar()
    return errores_modelo if not valido_modelo else []


def validar_alumno_completo(alumno: Alumno) -> tuple:
    """Valida que el alumno tenga todos los datos base requeridos."""
    errores = _validar_base(alumno)
    return (len(errores) == 0, errores)


def validar_alumno_para_certificado(alumno: Alumno) -> tuple:
    """Valida que el alumno tenga los datos necesarios para generar un certificado."""
    errores = _validar_base(alumno)
    
    if alumno.especialidad is None:
        errores.append("El alumno debe tener una especialidad asignada para generar el certificado")
    
    if alumno.tipo_documento is None:
        errores.append("El alumno debe tener un tipo de documento asignado")
    
    return (len(errores) == 0, errores)


def validar_alumno_para_ficha(alumno: Alumno) -> tuple:
    """Valida que el alumno tenga los datos necesarios para generar una ficha."""
    errores = _validar_base(alumno)
    
    if alumno.tipo_documento is None:
        errores.append("El alumno debe tener un tipo de documento asignado para generar la ficha")
    
    return (len(errores) == 0, errores)
