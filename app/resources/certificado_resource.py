import os
from flask import Blueprint, request, jsonify, send_file, current_app
from celery.result import AsyncResult
from app.tasks import tarea_generar_documento 

certificado_bp = Blueprint('certificado', __name__)


DIRECTORIO_GENERADOS = "/app/generated"


@certificado_bp.route('/generar', methods=['POST'])
def solicitar_generacion():
    data = request.get_json()
    
    
    if not data or 'alumno_id' not in data:
        return jsonify({"error": "Faltan datos. Se requiere 'alumno_id'"}), 400
        
    alumno_id = data.get('alumno_id')
    formato = data.get('formato', 'pdf') 

    if formato not in ['pdf', 'docx', 'odt']:
        return jsonify({"error": "Formato no soportado. Use: pdf, docx, odt"}), 400

    
    task = tarea_generar_documento.delay(alumno_id, formato)

    return jsonify({
        "mensaje": "Solicitud recibida. Procesando documento.",
        "task_id": task.id,
        "url_status": f"/api/v1/documentos/status/{task.id}"
    }), 202

@certificado_bp.route('/status/<task_id>', methods=['GET'])
def consultar_estado(task_id):
    task_result = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "estado": task_result.state
    }

    if task_result.state == 'SUCCESS':
        resultado = task_result.result
        filename = resultado.get('filename')
        
        response["mensaje"] = "Documento generado exitosamente."
        response["url_descarga"] = f"/api/v1/documentos/descargar/{filename}"
        
    elif task_result.state == 'FAILURE':
        response["mensaje"] = "Error al generar el documento."
        response["error"] = str(task_result.result)
    
    else:
        response["mensaje"] = "Procesando..."

    return jsonify(response)


@certificado_bp.route('/descargar/<filename>', methods=['GET'])
def descargar_archivo(filename):
    ruta_completa = os.path.join(DIRECTORIO_GENERADOS, filename)
    
    
    if not os.path.exists(ruta_completa):
        return jsonify({"error": "El archivo no existe o ha expirado."}), 404

   
    mimetype = 'application/pdf'
    if filename.endswith('.docx'):
        mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif filename.endswith('.odt'):
        mimetype = 'application/vnd.oasis.opendocument.text'

    return send_file(
        ruta_completa,
        mimetype=mimetype,
        as_attachment=True,
        download_name=filename
    )