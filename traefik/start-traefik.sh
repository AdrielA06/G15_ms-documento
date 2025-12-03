#!/bin/bash
# filepath: start-traefik.sh

echo "=== Iniciando configuración de Traefik ==="

# 1. Verificar que la red existe
if ! docker network inspect mired >/dev/null 2>&1; then
    echo "Creando red 'mired'..."
    docker network create mired
fi

# 2. Verificar certificados
if [ ! -f "traefik/certs/local-cert.pem" ]; then
    echo "Generando certificados..."
    cd traefik && ./generate-certs.sh && cd ..
fi

# 3. Crear directorio de logs
mkdir -p traefik/logs

# 4. Iniciar Traefik
echo "Iniciando Traefik..."
docker-compose -f docker-compose.traefik.yml up -d

# 5. Esperar a que Traefik esté listo
echo "Esperando a que Traefik esté listo..."
sleep 5

# 6. Iniciar servicios
echo "Iniciando servicios..."
docker-compose up -d

echo "=== Configuración completada ==="
echo ""
echo "URLs disponibles:"
echo "  - Dashboard: https://traefik.universidad.localhost"
echo "  - Documentos: https://documentos.universidad.localhost"
echo "  - Alumnos: https://alumnos.universidad.localhost"
echo "  - Académica: https://academica.universidad.localhost"
echo ""
echo "Credenciales Dashboard: admin/admin"