from app.exceptions import ServiceError, NotFoundError
from app.services.documento_service import documento_service

class CertificadoController:
    @staticmethod
    def obtener_certificado(id: int, tipo: str):
        return documento_service.generar_certificado_alumno_regular(id, tipo)

class ControladorService:
    def __init__(self, doc_srv=None):
        self.doc_srv = doc_srv or documento_service
    
    def get_academic_record(self, alumno_id: int):
        try:
            if hasattr(self.doc_srv, "get_by_alumno_id"):
                registro = self.doc_srv.get_by_alumno_id(alumno_id)
            elif hasattr(self.doc_srv, "obtener_registro"):
                registro = self.doc_srv.obtener_registro(alumno_id)
            elif hasattr(self.doc_srv, "get_academic_data"):
                registro = self.doc_srv.get_academic_data(alumno_id)
            else:
                raise ServiceError("Documento service no expone método para obtener registro académico")
            
            if not registro:
                raise NotFoundError(f"No se encontró registro académico para alumno {alumno_id}")
            
            return registro
        except (NotFoundError, ServiceError):
            raise
        except Exception as e:
            raise ServiceError(f"Error consultando registro académico: {e}")

controlador_service = ControladorService()
