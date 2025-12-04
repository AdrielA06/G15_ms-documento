from unittest.mock import patch, MagicMock
from app.services.documentos_office_service import DocumentService
from app.services.alumno_service import AlumnoService


def test_formatos_disponibles():
    formatos = DocumentService.formatos_disponibles()
    assert 'pdf' in formatos
    assert 'docx' in formatos
    assert 'odt' in formatos


def test_formatos_tienen_content_type():
    assert DocumentService.FORMATOS['pdf'] == ('application/pdf', 'pdf')
    assert DocumentService.FORMATOS['docx'] == ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx')
    assert DocumentService.FORMATOS['odt'] == ('application/vnd.oasis.opendocument.text', 'odt')


def test_generar_ficha_formato_invalido():
    service = DocumentService()
    alumno = {"legajo": "12345", "nombre_completo": "Test"}
    
    try:
        service.generar_ficha_alumno(alumno, "jpg")
        assert False, "Debería lanzar ValueError"
    except ValueError as e:
        assert "Formato no soportado" in str(e)


@patch('app.services.documentos_office_service.obtener_tipo_documento')
def test_generar_ficha_alumno_pdf(mock_obtener_tipo):

    mock_doc_class = MagicMock()
    mock_doc_class.generar.return_value = MagicMock(getvalue=lambda: b'contenido_pdf')
    mock_obtener_tipo.return_value = mock_doc_class
    
    service = DocumentService()
    
    alumno_service = AlumnoService()

    alumno_id = 1

    alumno = alumno_service.obtener_alumno_por_id(alumno_id)

    alumno_para_ficha = {
        "legajo": alumno.nro_legajo,
        "nombre_completo": alumno.nombre_completo,
        "numero_documento": alumno.nro_documento,
        "especialidad": alumno.especialidad_nombre,
        "anio_cursado": "3ro"
    }
    
    content, content_type, extension = service.generar_ficha_alumno(alumno_para_ficha, "pdf")
    
    assert content == b'contenido_pdf'
    assert content_type == 'application/pdf'
    assert extension == 'pdf'
    mock_obtener_tipo.assert_called_once_with("pdf")