def question_schema(question)->dict:
    """Convierte un documento de base de datos a un diccionario,
       manejando conversiones y valores nulos."""
    return {
        "id"                : str(question["_id"]),
        "pregunta"          : str(question.get("pregunta", "")),
        "opciones"          : list(question.get("opciones", [])),
        "respuesta_correcta": str(question.get("respuesta_correcta", "")),
        "categoria"         : str(question.get("categoria", "")),
        "puntos_pregunta"   : int(question.get("puntos_pregunta", "")),
        "nivel"             : str(question.get("nivel", "")),
        "consecutiva"       : int(question.get("consecutiva", "")),
        "usuario_carga"     : str(question.get("usuario_carga", "")),
        "fecha_carga"       : question.get("fecha_carga", ""),
        "tipo"              : str(question.get("tipo", "")),
        "estado"            : bool(question.get("estado", False))
    }

def schema_request(request) -> dict:
    """Valida los datos de entrada y los convierte a un diccionario limpio."""
    return {
        "pregunta"          : str(request.get("pregunta", "")),
        "opciones"          : list(request.get("opciones", [])),
        "respuesta_correcta": str(request.get("respuesta_correcta", "")),
        "nivel"             : str(request.get("nivel", "")),
        "categoria"         : str(request.get("categoria", {})),
    }

def many_question_schema(questions)->list:
    return [question_schema(question) for question in questions]

def many_request_schema(requests)->list:
    return [schema_request(request) for request in requests]