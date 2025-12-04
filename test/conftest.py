import pytest
import os
import shutil
from app import create_app

@pytest.fixture
def app():
    
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    
    
    app.config['UPLOAD_FOLDER'] = '/tmp/test_generated'
    
   
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    yield app

    
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])

@pytest.fixture
def client(app):
    return app.test_client()