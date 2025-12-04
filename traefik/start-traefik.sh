echo "=== Iniciando configuración de Traefik ==="

if ! docker network inspect mired >/dev/null 2>&1; then
    echo "Creando red 'mired'..."
    docker network create mired
fi

if [ ! -f "traefik/certs/local-cert.pem" ]; then
    echo "Generando certificados..."
    cd traefik && ./generate-certs.sh && cd ..
fi

mkdir -p traefik/logs

echo "Iniciando Traefik..."
docker-compose -f docker-compose.traefik.yml up -d

echo "Esperando a que Traefik esté listo..."
sleep 5

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