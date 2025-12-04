import json

def test_endpoint_generar_ok(client):
   
    payload = {
        "alumno_id": 999,
        "formato": "pdf"
    }
    
    response = client.post('/api/v1/documentos/generar', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert "url_descarga" in data
    assert "generado exitosamente" in data["mensaje"]

def test_endpoint_generar_falta_dato(client):
   
    payload = {
        "formato": "pdf"
    }
    
    response = client.post('/api/v1/documentos/generar', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 400
    assert "Faltan datos" in response.get_json()["error"]

def test_endpoint_generar_formato_invalido(client):
    
    payload = {
        "alumno_id": 999,
        "formato": "jpg" 
    }
    
    response = client.post('/api/v1/documentos/generar', 
                           data=json.dumps(payload),
                           content_type='application/json')
    
    assert response.status_code == 400

def test_endpoint_descargar_no_existente(client):
   
    response = client.get('/api/v1/documentos/descargar/archivo_fantasma.pdf')
    assert response.status_code == 404