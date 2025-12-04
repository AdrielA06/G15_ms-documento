import pytest
import os
import shutil
import tempfile
from app import create_app

@pytest.fixture
def app():
    
    os.environ['FLASK_CONTEXT'] = 'testing'
    app = create_app()
    
    
    test_upload_dir = tempfile.mkdtemp(prefix='flask_test_')
    app.config['UPLOAD_FOLDER'] = test_upload_dir
    app.config['TESTING'] = True
    
    
    if not os.path.exists(test_upload_dir):
        os.makedirs(test_upload_dir)

    yield app

   
    if os.path.exists(test_upload_dir):
        shutil.rmtree(test_upload_dir)

@pytest.fixture
def client(app):
    return app.test_client()