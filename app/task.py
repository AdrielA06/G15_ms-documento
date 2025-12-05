import os
from app import celery
from app.services.controlador_service import CertificadoController

DIRECTORIO_GENERADOS = "/app/generated"

@celery.task(bind=True)
def tarea_generar_documento(self, alumno_id: int, formato: str):

    try:
        archivo_io = CertificadoController.obtener_certificado(alumno_id, formato)
        
        nombre_archivo = f"certificado_{alumno_id}.{formato}"
        ruta_completa = os.path.join(DIRECTORIO_GENERADOS, nombre_archivo)
        
        os.makedirs(DIRECTORIO_GENERADOS, exist_ok=True)
        
        with open(ruta_completa, "wb") as f:
            f.write(archivo_io.getbuffer())
            
        return {
            "status": "success", 
            "filename": nombre_archivo,
            "formato": formato
        }

    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e
