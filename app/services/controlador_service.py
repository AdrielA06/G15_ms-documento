from app.services import AlumnoService


class CertificadoController:
    @staticmethod
    def obtener_certificado(id: int, tipo: str):
        return AlumnoService.generar_certificado_alumno_regular(id, tipo)
