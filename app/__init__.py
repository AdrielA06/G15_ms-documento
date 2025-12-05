import os
from flask import Flask
from app.config.config import factory
from app.resources.certificado_resource import certificado_bp
from app.resources.ficha_alumno_resource import ficha_alumno_bp
from app.resources.home import home
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def create_app():
    
    env = os.environ.get('FLASK_CONTEXT', os.environ.get('FLASK_ENV', 'development'))

    app = Flask(__name__)
    app.config.from_object(factory(env))
    
    app.register_blueprint(certificado_bp, url_prefix='/api/v1/documentos')
    app.register_blueprint(ficha_alumno_bp, url_prefix='/api/v1/documentos')
    app.register_blueprint(home, url_prefix='/')

    logger.info(f"Microservicio de Documentos iniciado en entorno: {env}")

    return app