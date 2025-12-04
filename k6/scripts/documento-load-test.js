import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const certificadoTrend = new Trend('certificado_duration');

export const options = {
    scenarios: {
        smoke: {
            executor: 'constant-vus',
            vus: 1,
            duration: '30s',
            startTime: '0s',
            tags: { test_type: 'smoke' },
        },
        load: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '1m', target: 10 },  // Subir a 10 usuarios
                { duration: '3m', target: 10 },  // Mantener 10 usuarios
                { duration: '1m', target: 0 },   // Bajar a 0
            ],
            startTime: '30s',
            tags: { test_type: 'load' },
        },
        stress: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '2m', target: 50 },
                { duration: '5m', target: 50 },
                { duration: '2m', target: 100 },
                { duration: '5m', target: 100 },
                { duration: '2m', target: 0 },
            ],
            startTime: '6m',
            tags: { test_type: 'stress' },
        },
    },
    thresholds: {
        http_req_duration: ['p(95)<500'],
        errors: ['rate<0.1'],
        'certificado_duration': ['p(95)<1000'],
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://documentos.universidad.localhost';

export function setup() {
    const res = http.get(`${BASE_URL}/`);
    check(res, {
        'servicio disponible': (r) => r.status === 200,
    });
}

export default function () {
    const healthRes = http.get(`${BASE_URL}/`);
    check(healthRes, {
        'health check OK': (r) => r.status === 200,
    });
    errorRate.add(healthRes.status !== 200);

    sleep(1);

    const payload = JSON.stringify({
        alumno_id: Math.floor(Math.random() * 1000) + 1,
        formato: 'pdf',
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const startTime = Date.now();
    const certRes = http.post(
        `${BASE_URL}/api/v1/documentos/generar`,
        payload,
        params
    );
    certificadoTrend.add(Date.now() - startTime);

    check(certRes, {
        'certificado generado': (r) => r.status === 200 || r.status === 201,
        'respuesta tiene contenido': (r) => r.body.length > 0,
    });
    errorRate.add(certRes.status >= 400);

    sleep(2);

    const formatosRes = http.get(`${BASE_URL}/api/v1/documentos/formatos`);
    check(formatosRes, {
        'formatos obtenidos': (r) => r.status === 200,
        'contiene pdf': (r) => r.body.includes('pdf'),
    });

    sleep(1);
}

export function teardown(data) {
    console.log('Pruebas de carga finalizadas');
}