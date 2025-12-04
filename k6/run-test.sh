#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="${SCRIPT_DIR}/results"

# Crear directorio de resultados si no existe
mkdir -p "${RESULTS_DIR}"

# Timestamp para archivos
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo -e "${YELLOW}=== Iniciando pruebas de carga K6 ===${NC}"

# Verificar si k6 está instalado localmente o usar Docker
if command -v k6 &> /dev/null; then
    echo -e "${GREEN}Usando K6 local${NC}"
    K6_CMD="k6"
else
    echo -e "${YELLOW}Usando K6 via Docker${NC}"
    K6_CMD="docker run --rm -i --network mired -v ${SCRIPT_DIR}/scripts:/scripts -v ${RESULTS_DIR}:/results grafana/k6"
fi

# Función para ejecutar prueba
run_test() {
    local script=$1
    local output_file="${RESULTS_DIR}/${script%.js}_${TIMESTAMP}.json"
    
    echo -e "\n${YELLOW}Ejecutando: ${script}${NC}"
    
    if [ "$K6_CMD" = "k6" ]; then
        k6 run \
            --env BASE_URL="${BASE_URL:-https://documentos.universidad.localhost}" \
            --out json="${output_file}" \
            "${SCRIPT_DIR}/scripts/${script}"
    else
        $K6_CMD run \
            --env BASE_URL="${BASE_URL:-http://documentos-service:5000}" \
            --out json="/results/${script%.js}_${TIMESTAMP}.json" \
            "/scripts/${script}"
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ ${script} completado${NC}"
    else
        echo -e "${RED}✗ ${script} falló${NC}"
    fi
}

# Menú de opciones
case "${1:-all}" in
    smoke)
        echo "Ejecutando prueba de humo..."
        run_test "documento-load-test.js"
        ;;
    load)
        echo "Ejecutando prueba de carga..."
        run_test "documento-load-test.js"
        ;;
    ficha)
        echo "Ejecutando prueba de ficha alumno..."
        run_test "ficha-alumno-test.js"
        ;;
    all)
        echo "Ejecutando todas las pruebas..."
        run_test "documento-load-test.js"
        run_test "ficha-alumno-test.js"
        ;;
    *)
        echo "Uso: $0 {smoke|load|ficha|all}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}=== Pruebas finalizadas ===${NC}"
echo -e "Resultados guardados en: ${RESULTS_DIR}"