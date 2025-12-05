# Microservicio de Documentación (SysAcad)

# Integrantes:

# ALONSO, Adriel
# BETTIOL, Giuliana
# MARTINEZ OLDANI, Jimena
# RUIZ ANDREOLA, Alejandro Raúl
# SANCHEZ, Juan
# VELAZCO, Franco
# VULCANO, Candela

Este microservicio se encarga de la generación de documentos (PDF, DOCX, ODT) para el sistema SysAcad. Está construido con Python (Flask), utiliza Redis para caché/mensajería y es servido mediante Granian detrás de un proxy Traefik.

## Requisitos Previos

*   *Docker* y *Docker Compose* instalados.
*   *Python 3.12+* (para desarrollo local).
*   *PowerShell* (si estás en Windows) o Terminal Bash.

---

## Gestión de Dependencias con uv

Este proyecto utiliza [uv](https://github.com/astral-sh/uv) para la gestión rápida de paquetes y entornos virtuales.

### 1. Instalación de uv

*Windows (PowerShell como Administrador):*
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Si estás en Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear entorno virtual
uv venv

# Sincronizar dependencias
uv sync

# Ejecución con Docker

# Red externa
docker network create mired

# Levantar Traefik
docker-compose -f docker-compose.traefik.yml up -d

# Levantar Redis
docker-compose -f redis/docker-compose.yml up -d

# Levantar el Microservicio
docker-compose up -d --build

# Pruebas de Carga con K6
# Para uso en Linux/Bash:

chmod +x k6/run-test.sh
./k6/run-test.sh smoke
./k6/run-test.sh load

# Para ejecución manual en Docker

docker run --rm --network mired -v ${PWD}/k6/scripts:/scripts -v ${PWD}/k6/results:/results grafana/k6 run -e BASE_URL=http://documentos.universidad.localhost:5000 /scripts/ficha-alumno-test.js

# En donde dice ficha-alumno-test.js, se refiere al archivo que se está ejecutando para el test.
