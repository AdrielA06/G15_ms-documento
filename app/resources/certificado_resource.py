from flask import Blueprint, send_file
from app.services.certificate_service import CertificateService

certificado_bp = Blueprint('certificado', __name__)

FORMATOS_CERTIFICADO = {
    'pdf': {
        'mime_type': 'application/pdf',
        'extension': 'certificado.pdf',
        'as_attachment': False
    },
    'odt': {
        'mime_type': 'application/vnd.oasis.opendocument.text',
        'extension': 'certificado.odt',
        'as_attachment': True
    },
    'docx': {
        'mime_type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'extension': 'certificado.docx',
        'as_attachment': True
    }
}

@certificado_bp.route('/certificado/<int:id>/<formato>', methods=['GET'])
def certificado(id: int, formato: str):
    formato = formato.lower()
    
    if formato not in FORMATOS_CERTIFICADO:
        return {
            "error": f"Formato no soportado. Disponibles: {list(FORMATOS_CERTIFICADO.keys())}"
        }, 400
    
    try:
        config = FORMATOS_CERTIFICADO[formato]
        documento_io = CertificateService.generar_certificado_alumno_regular(id, formato)
        
        if not documento_io:
            return {"error": f"No se pudo generar el certificado en formato {formato}"}, 500
        
        return send_file(
            documento_io,
            mimetype=config['mime_type'],
            as_attachment=config['as_attachment'],
            download_name=config['extension']
        )
    except Exception as e:
        return {"error": str(e)}, 500