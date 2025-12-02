from flask import Blueprint, request, make_response
from flask_restful import Api, Resource
from app.services.documentos_office_service import DocumentService
from app.services.alumno_service import (
    AlumnoService, 
    ServiceConnectionError,
    AlumnoNotFoundError
)


ficha_alumno_bp = Blueprint("ficha_alumno", __name__)
api = Api(ficha_alumno_bp)


class FichaAlumnoResource(Resource):
    def __init__(self):
        self.document_service = DocumentService()
        self.alumno_service = AlumnoService()
    
    def get(self, legajo: int):
        format = request.args.get("format", "pdf").lower()

        if format not in DocumentService.formatos_disponibles():
            return {
                "error": f"Formato no soportado. Disponibles: {DocumentService.formatos_disponibles()}"
            }, 400
        
        try:
            alumno = self.alumno_service.obtener_alumno_por_legajo(legajo)

            content, content_type, extension = self.document_service.generar_ficha_alumno(
                alumno=alumno,
                format=format
            )

            response = make_response(content)
            response.headers["Content-Type"] = content_type
            response.headers["Content-Disposition"] = (
                f"attachment; filename=ficha_alumno_{legajo}.{extension}"
            )
            
            return response
        
        except AlumnoNotFoundError:
            return {"error": f"Alumno con legajo {legajo} no encontrado"}, 404
        except ServiceConnectionError as e:
            return {"error": str(e)}, 503
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"Error interno: {str(e)}"}, 500


class FormatosResource(Resource):
    """Resource para obtener formatos disponibles."""
    
    def get(self):
        """Retorna los formatos disponibles."""
        return {
            "formatos": DocumentService.formatos_disponibles(),
            "default": "pdf"
        }


api.add_resource(FichaAlumnoResource, "/ficha/<int:legajo>")
api.add_resource(FormatosResource, "/formatos")