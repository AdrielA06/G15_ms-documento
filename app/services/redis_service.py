import redis
from app.config.config import Config

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            decode_responses=True
        )
    
    def cache_certificado(self, key, valor, ttl=3600):
        self.client.setex(key, ttl, valor)
    
    def get_cached(self, key):
        return self.client.get(key)

redis_service = RedisService()