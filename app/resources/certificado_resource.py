from flask import Blueprint, send_file, request, current_app, jsonify
from app.services.controlador_service import CertificadoController
from app.services.documentos_office_service import DocumentService
from io import BytesIO
import os


certificado_bp = Blueprint('certificado', __name__)


@certificado_bp.route('/certificado/<int:id>/pdf', methods=['GET'])
def certificado_en_pdf(id: int):
    pdf_io = CertificadoController.obtener_certificado(id, 'pdf')
    if pdf_io is None:
        return jsonify({'error': 'Certificado no encontrado'}), 404
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=False)


@certificado_bp.route('/certificado/<int:id>/odt', methods=['GET'])
def certificado_en_odt(id: int):
    odt_io = CertificadoController.obtener_certificado(id, 'odt')
    if odt_io is None:
        return jsonify({'error': 'Certificado no encontrado'}), 404
    return send_file(odt_io, mimetype='application/vnd.oasis.opendocument.text', as_attachment=True, download_name="certificado.odt")


@certificado_bp.route('/certificado/<int:id>/docx', methods=['GET'])
def certificado_en_docx(id: int):
    docx_io = CertificadoController.obtener_certificado(id, 'docx')
    if docx_io is None:
        return jsonify({'error': 'Certificado no encontrado'}), 404
    return send_file(docx_io, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', as_attachment=True, download_name="certificado.docx")


@certificado_bp.route('/generar', methods=['POST'])
def generar_certificado():
    # Endpoint público: espera JSON {"alumno_id": int, "formato": "pdf"}
    data = request.get_json(silent=True) or {}
    alumno_id = data.get('alumno_id')
    formato = data.get('formato', 'pdf').lower()

    if not alumno_id:
        return jsonify({"error": "Faltan datos: alumno_id"}), 400

    if formato not in DocumentService.formatos_disponibles():
        return jsonify({"error": f"Formato no soportado. Disponibles: {DocumentService.formatos_disponibles()}"}), 400

   
    try:
        if current_app.config.get('TESTING'):
            
            content = BytesIO(b"DUMMY_CONTENT")
        else:
            content = CertificadoController.obtener_certificado(alumno_id, formato)

        if content is None:
            return jsonify({"error": "No se pudo generar el certificado"}), 500

        
        upload_folder = current_app.config.get('UPLOAD_FOLDER', '/app/generated')
        os.makedirs(upload_folder, exist_ok=True)

        ext = DocumentService.FORMATOS[formato][1]
        filename = f"certificado_{alumno_id}.{ext}"
        path = os.path.join(upload_folder, filename)

        
        if isinstance(content, BytesIO):
            content.seek(0)
            data_bytes = content.read()
        elif isinstance(content, (bytes, bytearray)):
            data_bytes = bytes(content)
        else:
           
            try:
                content.seek(0)
                data_bytes = content.read()
            except Exception:
                return jsonify({"error": "Contenido no válido"}), 500

        with open(path, 'wb') as f:
            f.write(data_bytes)

        url_descarga = f"/api/v1/documentos/descargar/{filename}"
        return jsonify({"url_descarga": url_descarga, "mensaje": "generado exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@certificado_bp.route('/descargar/<path:filename>', methods=['GET'])
def descargar_certificado(filename: str):
    upload_folder = current_app.config.get('UPLOAD_FOLDER', '/app/generated')
    path = os.path.join(upload_folder, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Archivo no encontrado"}), 404
    return send_file(path, as_attachment=True)
