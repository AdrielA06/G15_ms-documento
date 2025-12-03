import logging
import os
from flask import Flask, jsonify, request
from celery import Celery  # Import necesario para la cola de tareas
from app.config import config
from .exceptions import AppError, ValidationError, NotFoundError, ServiceError

# --- INSTANCIA GLOBAL DE CELERY ---
# Se define fuera de create_app para que pueda ser importada por tasks.py
celery = Celery(__name__)

def create_app() -> Flask:
    """
    Application Factory para inicializar Flask y sus extensiones.
    """
    app_context = os.getenv('FLASK_CONTEXT')
    
    # Inicialización de Flask
    app = Flask(__name__, template_folder='template', static_folder='static')

    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    # --- CONFIGURACIÓN DE CELERY ---
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    from app.resources import home, certificado_bp

    app.register_blueprint(home, url_prefix='/api/v1')
    
    app.register_blueprint(certificado_bp, url_prefix='/api/v1/documentos')

    # Registro de Manejadores de Errores
    register_errorhandlers(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app


# --- MANEJADORES DE ERRORES ---

def register_errorhandlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err):
        return jsonify(err.to_dict()), getattr(err, "status_code", 500)

    @app.errorhandler(404)
    def handle_404(err):
        body = {"error": "NotFound", "message": "Recurso no encontrado"}
        return jsonify(body), 404

    @app.errorhandler(405)
    def handle_405(err):
        body = {"error": "MethodNotAllowed", "message": "Método no permitido en este recurso"}
        return jsonify(body), 405

    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        logging.exception("Unexpected error")
        body = {"error": "InternalServerError", "message": "Ha ocurrido un error inesperado."}
        return jsonify(body), 500

# --- UTILIDADES ---

def validar_payload(payload):
    """
    Valida que el payload contenga los campos obligatorios.
    """
    faltantes = [f for f in ("nombre","apellidos","dni") if not payload.get(f)]
    if faltantes:
        raise ValidationError("Faltan campos obligatorios", payload={"missing": faltantes})