import requests
from app.config.config import Config
from app.models.alumno import Alumno
from app.mapping.alumno_mapping import map_to_alumno
from app.exceptions import ServiceError, NotFoundError

class ServiceConnectionError(Exception):
    pass

class AlumnoNotFoundError(Exception):
    pass

class AlumnoService:
    def __init__(self):
        self.base_url = Config.ALUMNOS_HOST
        self.timeout = 10
    
    def _hacer_request(self, endpoint: str) -> dict:
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise AlumnoNotFoundError(f"Recurso no encontrado: {endpoint}")
            else:
                response.raise_for_status()
                
        except requests.ConnectionError:
            raise ServiceConnectionError(
                f"No se pudo conectar con el servicio de alumnos en {self.base_url}"
            )
        except requests.Timeout:
            raise ServiceConnectionError(
                f"Timeout al conectar con el servicio de alumnos"
            )
        except requests.RequestException as e:
            raise ServiceConnectionError(
                f"Error en la petición al servicio de alumnos: {e}"
            )
    
    def obtener_alumno_por_legajo(self, legajo: int) -> Alumno:
        data = self._hacer_request(f"/api/v1/alumnos/legajo/{legajo}")
        return map_to_alumno(data)
    
    def obtener_alumno_por_id(self, alumno_id: int) -> Alumno:
        data = self._hacer_request(f"/api/v1/alumnos/{alumno_id}")
        return map_to_alumno(data)
    
    def get_by_id(self, alumno_id: int) -> Alumno:
        try:
            return self.obtener_alumno_por_id(alumno_id)
        except AlumnoNotFoundError:
            return None
        except ServiceConnectionError as e:
            raise ServiceError(f"Error conectando con servicio de alumnos: {e}")
    
    def obtener_todos_alumnos(self) -> list:
        data = self._hacer_request("/api/v1/alumnos")
        return [map_to_alumno(item) for item in data]

alumno_service = AlumnoService()