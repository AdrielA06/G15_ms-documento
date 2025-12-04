import os
from dotenv import load_dotenv

load_dotenv()

class Config:
   
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/generated')
    ALUMNOS_HOST = os.getenv('ALUMNOS_HOST', 'http://alumno-service')
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

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