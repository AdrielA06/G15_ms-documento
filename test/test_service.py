import os
from unittest.mock import patch
from app.services.documento_service import generar_documento_core


@patch('app.services.documento_service.DIRECTORIO_GENERADOS', '/tmp/test_service_generated')
def test_generar_documento_exitoso():
   
    os.makedirs('/tmp/test_service_generated', exist_ok=True)
    
    alumno_id = 123
    formato = 'pdf'
    filename = generar_documento_core(alumno_id, formato)
    
    assert filename == f"certificado_alumno_{alumno_id}.{formato}"
    assert os.path.exists(f"/tmp/test_service_generated/{filename}")

    if os.path.exists('/tmp/test_service_generated'):
        import shutil
        shutil.rmtree('/tmp/test_service_generated')