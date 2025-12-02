from dataclasses import dataclass
from typing import Any

from ..exceptions import ValidationError, NotFoundError, ServiceError
from . import alumno_service, certificate_service


@dataclass
class CertificateRequest:
    nombre: str
    apellidos: str
    dni: str
    opciones: Any = None


@dataclass
class CertificateResult:
    success: bool
    mensaje: str
    certificado: Any = None


class OrquestadorService:

    def __init__(self, alumno_srv=None, cert_srv=None):
        self.alumno_srv = alumno_srv or alumno_service
        self.cert_srv = cert_srv or certificate_service

    def generar_certificado(self, alumno_id: int, opciones=None) -> CertificateResult:
        if hasattr(self.alumno_srv, "get_by_id"):
            alumno = self.alumno_srv.get_by_id(alumno_id)
        elif hasattr(self.alumno_srv, "find_by_id"):
            alumno = self.alumno_srv.find_by_id(alumno_id)
        else:
            raise ServiceError("Alumno service no expone método de consulta por id")

        if alumno is None:
            raise NotFoundError(f"Alumno con id {alumno_id} no encontrado")

        if not getattr(alumno, "nombre", ""):
            raise ValidationError("Falta el nombre del alumno")
        if not getattr(alumno, "apellidos", ""):
            raise ValidationError("Faltan los apellidos del alumno")
        if not getattr(alumno, "dni", ""):
            raise ValidationError("Falta el dni del alumno")

        req = CertificateRequest(
            nombre=alumno.nombre,
            apellidos=alumno.apellidos,
            dni=alumno.dni,
            opciones=opciones
        )

        try:
            if hasattr(self.cert_srv, "create_certificate"):
                certificado = self.cert_srv.create_certificate(req)
            elif hasattr(self.cert_srv, "generate"):
                certificado = self.cert_srv.generate(req)
            else:
                raise ServiceError("Certificate service no expone create_certificate/generate")

            return CertificateResult(success=True, mensaje="Certificado generado", certificado=certificado)

        except (ValidationError, NotFoundError, ServiceError):
            raise
        except Exception as e:
            raise ServiceError(f"Error interno generando certificado: {e}")

orquestador_service = OrquestadorService()