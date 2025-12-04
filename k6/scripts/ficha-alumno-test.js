import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
    vus: 10,
    duration: '2m',
    thresholds: {
        http_req_duration: ['p(95)<800'],
        http_req_failed: ['rate<0.05'],
    },
};

const BASE_URL = __ENV.BASE_URL || 'https://documentos.universidad.localhost';

export default function () {
    const legajo = Math.floor(Math.random() * 10000) + 1;

    group('Ficha Alumno - PDF', () => {
        const res = http.get(`${BASE_URL}/api/v1/documentos/ficha/${legajo}?formato=pdf`);
        check(res, {
            'ficha PDF status 200 o 404': (r) => r.status === 200 || r.status === 404,
        });
    });

    sleep(1);

    group('Ficha Alumno - DOCX', () => {
        const res = http.get(`${BASE_URL}/api/v1/documentos/ficha/${legajo}?formato=docx`);
        check(res, {
            'ficha DOCX status 200 o 404': (r) => r.status === 200 || r.status === 404,
        });
    });

    sleep(1);

    group('Ficha Alumno - ODT', () => {
        const res = http.get(`${BASE_URL}/api/v1/documentos/ficha/${legajo}?formato=odt`);
        check(res, {
            'ficha ODT status 200 o 404': (r) => r.status === 200 || r.status === 404,
        });
    });

    sleep(2);
}