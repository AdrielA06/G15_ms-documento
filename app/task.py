import os
from app import celery
from app.services.controlador_service import CertificadoController

DIRECTORIO_GENERADOS = "/app/generated"

@celery.task(bind=True)
def tarea_generar_documento(self, alumno_id: int, formato: str):

    try:
        # 1. Llamamos a tu lógica de negocio existente
        archivo_io = CertificadoController.obtener_certificado(alumno_id, formato)
        
        # 2. Preparamos la ruta de guardado
        nombre_archivo = f"certificado_{alumno_id}.{formato}"
        ruta_completa = os.path.join(DIRECTORIO_GENERADOS, nombre_archivo)
        
        # Aseguramos que el directorio exista
        os.makedirs(DIRECTORIO_GENERADOS, exist_ok=True)
        
        # 3. Escribimos el archivo en el disco compartido
        with open(ruta_completa, "wb") as f:
            f.write(archivo_io.getbuffer())
            
        # 4. Retornamos datos útiles para el endpoint de status
        return {
            "status": "success", 
            "filename": nombre_archivo,
            "formato": formato
        }

    except Exception as e:
        # Si falla, registramos el error en la tarea
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise e