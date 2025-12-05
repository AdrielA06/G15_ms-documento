from dataclasses import dataclass, asdict
from typing import Any

from ..exceptions import ValidationError, NotFoundError, ServiceError
from . import alumno_service, controlador_service, documentos_office_service

@dataclass
class AlumnoInfo:
    nombre: str
    apellidos: str
    dni: str
    foto: Any = None

@dataclass
class AcademicInfo:
    curso: str
    notas: Any
    fechas: Any

@dataclass
class CertificatePayload:
    alumno: AlumnoInfo
    academic: AcademicInfo
    opciones: Any = None

@dataclass
class CertificateResult:
    success: bool
    mensaje: str
    documento: Any = None

class OrquestadorService:
    def __init__(self,
                 alumno_srv=None,
                 controlador_srv=None,
                 doc_srv=None):
        self.alumno_srv = alumno_srv or alumno_service
        self.controlador_srv = controlador_srv or controlador_service
        self.doc_srv = doc_srv or documentos_office_service

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

        alumno_info = AlumnoInfo(
            nombre=alumno.nombre,
            apellidos=alumno.apellidos,
            dni=alumno.dni,
            foto=getattr(alumno, "foto", None)
        )

        if hasattr(self.controlador_srv, "get_academic_record"):
            academic_raw = self.controlador_srv.get_academic_record(alumno_id)
        elif hasattr(self.controlador_srv, "get_by_alumno"):
            academic_raw = self.controlador_srv.get_by_alumno(alumno_id)
        else:
            raise ServiceError("Controlador service no expone método para obtener registro académico")

        if academic_raw is None:
            raise ServiceError("No se encontraron datos académicos para el alumno")

        curso = getattr(academic_raw, "curso", None) or getattr(academic_raw, "nombre_curso", None)
        notas = getattr(academic_raw, "notas", None)
        fechas = getattr(academic_raw, "fechas", None)

        if not curso:
            raise ValidationError("Falta el nombre del curso en los datos académicos")

        academic_info = AcademicInfo(curso=curso, notas=notas, fechas=fechas)

        payload = CertificatePayload(alumno=alumno_info, academic=academic_info, opciones=opciones)

        try:
            payload_dict = asdict(payload)
            if hasattr(self.doc_srv, "create_document"):
                documento = self.doc_srv.create_document(payload_dict)
            elif hasattr(self.doc_srv, "generate_document"):
                documento = self.doc_srv.generate_document(payload_dict)
            elif hasattr(self.doc_srv, "send"):
                documento = self.doc_srv.send(payload_dict)
            else:
                raise ServiceError("Documentos service no expone método para generar documentos")

            return CertificateResult(success=True, mensaje="Certificado generado", documento=documento)

        except (ValidationError, NotFoundError, ServiceError):
            raise
        except Exception as e:
            raise ServiceError(f"Error interno generando certificado: {e}")

orquestador_service = OrquestadorService()