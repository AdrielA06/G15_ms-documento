import os
from flask import Flask
from config import factory 
from app.utils.logger_config import setup_logger


logger = setup_logger(__name__)

def create_app():
   
    app = Flask(__name__)
    app.config.from_object(factory(env))
    from app.routes import certificado_bp 
    
    app.register_blueprint(certificado_bp, url_prefix='/api/v1/documentos')

    logger.info(f"Microservicio de Documentos iniciado en entorno: {env}")

    return app