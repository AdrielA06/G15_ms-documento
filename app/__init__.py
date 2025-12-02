import logging
import os
from flask import Flask
from app.config import config


def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)
    
    from app.resources import home, certificado_bp
    app.register_blueprint(home, url_prefix='/api/v1')
    app.register_blueprint(certificado_bp, url_prefix='/api/v1')

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app
