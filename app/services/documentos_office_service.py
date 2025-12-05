from abc import ABC, abstractmethod
from io import BytesIO
import os
from flask import current_app, render_template
from python_odt_template import ODTTemplate
from weasyprint import HTML
from python_odt_template.jinja import get_odt_renderer
from docxtpl import DocxTemplate
import jinja2
from enum import Enum

class FormatoDocumento(Enum):
    PDF = ('application/pdf', 'pdf')
    DOCX = ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx')
    ODT = ('application/vnd.oasis.opendocument.text', 'odt')
    
    def obtener_mime_type(self):
        return self[0]
    
    def obtener_extension(self):
        return self[1]

class DocumentService:
    @staticmethod
    def formatos_disponibles():
        return [formato.name.lower() for formato in FormatoDocumento]
    
    def generar_ficha_alumno(self, alumno: dict, format: str = "pdf"):
        documento_class = obtener_tipo_documento(format)
        if not documento_class:
            raise ValueError(f"Formato no soportado: {format}")
        
        context_legajo = alumno.get("legajo")
        context_nombre = alumno.get("nombre_completo")
        context_documento = alumno.get("numero_documento")
        context_especialidad = alumno.get("especialidad")
        context_anio = alumno.get("anio_cursado")
        
        content_io = documento_class.generar(
            carpeta="fichas",
            plantilla="ficha_alumno",
            legajo=context_legajo,
            nombre_completo=context_nombre,
            numero_documento=context_documento,
            especialidad=context_especialidad,
            anio_cursado=context_anio
        )
        
        formato = FormatoDocumento[format.upper()]
        content_type = formato.obtener_mime_type()
        extension = formato.obtener_extension()
        return content_io.getvalue(), content_type, extension

class Document(ABC):
    @staticmethod
    @abstractmethod
    def generar(carpeta: str, plantilla: str, **kwargs) -> BytesIO:
        pass

class PDFDocument(Document):
    @staticmethod
    def generar(carpeta: str, plantilla: str, **kwargs) -> BytesIO:
        base_path = current_app.root_path.replace('\\', '/')
        base_url = f"file:///{base_path}"

        render_context = kwargs.copy()
        render_context["url_base"] = base_url

        html_string = render_template(f"{carpeta}/{plantilla}.html", **render_context)
        bytes_data = HTML(string=html_string, base_url=base_url).write_pdf()
        pdf_io = BytesIO(bytes_data)
        return pdf_io

class ODTDocument(Document):
    @staticmethod
    def generar(carpeta: str, plantilla: str, **kwargs) -> BytesIO:
        templates_root = os.path.join(current_app.root_path, current_app.template_folder)
        path_template = os.path.join(templates_root, carpeta, f"{plantilla}.odt")

        media_path = current_app.static_folder
        odt_renderer = get_odt_renderer(media_path=media_path)

        odt_io = BytesIO()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.odt', delete=False) as temp_file:
            temp_path = temp_file.name

        with ODTTemplate(path_template) as template:
            odt_renderer.render(template, context=kwargs)
            template.pack(temp_path)
            with open(temp_path, 'rb') as f:
                odt_io.write(f.read())

        os.unlink(temp_path)
        odt_io.seek(0)
        return odt_io

class DOCXDocument(Document):
    @staticmethod
    def generar(carpeta: str, plantilla: str, **kwargs) -> BytesIO:
        templates_root = os.path.join(current_app.root_path, current_app.template_folder)
        path_template = os.path.join(templates_root, carpeta, f"{plantilla}.docx")

        doc = DocxTemplate(path_template)

        docx_io = BytesIO()
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_path = temp_file.name

        jinja_env = jinja2.Environment()
        render_context = kwargs.copy()
        base_path = current_app.root_path.replace('\\', '/')
        render_context["url_base"] = "file:///" + base_path

        doc.render(render_context, jinja_env)
        doc.save(temp_path)
        with open(temp_path, 'rb') as f:
            docx_io.write(f.read())

        os.unlink(temp_path)
        docx_io.seek(0)
        return docx_io

def obtener_tipo_documento(tipo: str):
    if tipo.upper() == 'PDF':
        return PDFDocument
    elif tipo.upper() == 'ODT':
        return ODTDocument
    elif tipo.upper() == 'DOCX':
        return DOCXDocument
    return None

documento_service = DocumentService()
