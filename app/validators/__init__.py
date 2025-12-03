from .alumno_validator import (
    validar_alumno_completo,
    validar_alumno_para_certificado,
    validar_alumno_para_ficha
)
from .especialidad_validator import (
    validar_especialidad_completa,
    validar_especialidad_para_certificado
)
from .tipo_documento_validator import validar_tipo_documento_completo

__all__ = [
    'validar_alumno_completo',
    'validar_alumno_para_certificado',
    'validar_alumno_para_ficha',
    'validar_especialidad_completa',
    'validar_especialidad_para_certificado',
    'validar_tipo_documento_completo'
]