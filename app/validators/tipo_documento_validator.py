from app.models.tipodocumento import TipoDocumento


def validar_tipo_documento_completo(tipo_documento: TipoDocumento) -> tuple:
    errores = []
    
    valido_modelo, errores_modelo = tipo_documento.validar()
    
    if not valido_modelo:
        errores.extend(errores_modelo)
    
    return (len(errores) == 0, errores)