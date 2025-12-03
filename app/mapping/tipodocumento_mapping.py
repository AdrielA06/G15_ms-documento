from app.models.tipodocumento import TipoDocumento

def map_to_tipo_documento(data) -> TipoDocumento:
    tipo = TipoDocumento()
    
    tipo.id = data.get("id", 0)
    tipo.sigla = data.get("sigla", "")
    tipo.nombre = data.get("nombre", "")
    tipo.descripcion = data.get("descripcion", "")
    
    if "datos_extra" in data:
        tipo.datos_extra = data["datos_extra"]
    
    return tipo
