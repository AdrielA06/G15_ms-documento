import logging
import os
from flask import Flask
from celery import Celery  
from app.config import config
celery = Celery(__name__)

def create_app() -> Flask:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def _call_(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    
    from app.resources import home, certificado_bp
    app.register_blueprint(home, url_prefix='/api/v1')
    app.register_blueprint(certificado_bp, url_prefix='/api/v1')

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app