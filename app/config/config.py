import os
from dotenv import load_dotenv

load_dotenv()

class Config:
   
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/generated')

class DevelopmentConfig(Config):
    
    DEBUG = True
    
class ProductionConfig(Config):
   
    DEBUG = False

class TestingConfig(Config):
    
    TESTING = True

def factory(env):
    envs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    return envs.get(env, DevelopmentConfig)