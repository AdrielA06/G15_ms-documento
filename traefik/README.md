# Configuración de Traefik

## Estructura de archivos

```
traefik/
├── traefik.yml          # Configuración estática principal
├── generate-certs.sh    # Script para generar certificados
├── README.md            # Esta documentación
├── config/
│   ├── tls.yml          # Configuración TLS
│   ├── security.yml     # Middlewares de seguridad
│   ├── middlewares.yml  # Circuit breakers y retry
│   └── routers.yml      # Routers adicionales
├── certs/
│   ├── local-cert.pem   # Certificado (generado)
│   └── local-key.pem    # Clave privada (generada)
└── logs/
    └── access.log       # Logs de acceso
```

## Inicio rápido

```bash
# 1. Dar permisos al script
chmod +x start-traefik.sh

# 2. Ejecutar
./start-traefik.sh
```

## URLs de servicios

| Servicio | URL |
|----------|-----|
| Dashboard Traefik | https://traefik.universidad.localhost |
| Documentos | https://documentos.universidad.localhost |
| Alumnos | https://alumnos.universidad.localhost |
| Académica | https://academica.universidad.localhost |

## Middlewares configurados

- **Circuit Breaker**: Protección contra fallos en cascada
- **Retry**: Reintentos automáticos (4 intentos)
- **Rate Limit**: 100 req/s con burst de 50
- **Secure Headers**: Headers de seguridad HTTP
- **Compress**: Compresión gzip

## Comandos útiles

```bash
# Ver logs de Traefik
docker logs -f traefik

# Reiniciar Traefik
docker-compose -f docker-compose.traefik.yml restart

# Ver estado de routers
curl -s http://localhost:8080/api/http/routers | jq
```