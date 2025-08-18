from datetime import datetime
from typing import List, Optional, Dict
from db.models.questions import QuestionRequest

def category_question_schema(categoria: Dict) -> Dict:
    """Convierte un diccionario de categoría, manejando valores nulos."""
    return {
        "categoria": str(categoria.get("categoria", "")),
        "sub_categoria": str(categoria.get("sub_categoria", None)),
        "micro_categoria": str(categoria.get("micro_categoria", None)),
        "nano_categoria": str(categoria.get("nano_categoria", None))
    }
    
def question_schema(question)->dict:
    """Convierte un documento de base de datos a un diccionario,
       manejando conversiones y valores nulos."""
    return {
        "id": str(question["_id"]),
        "pregunta": str(question.get("pregunta", "")),
        "opciones": list(question.get("opciones", [])),
        "respuesta_correcta": str(question.get("respuesta_correcta", "")),
        "categoria": category_question_schema(question.get("categoria", {})),
        "puntos_pregunta" : int(question.get("puntos", "")),
        "nivel"  : str(question.get("nivel", "")),
        "usuario_carga": str(question.get("usuario_carga", "")),
        "fecha_carga": question.get("fecha_carga"),
        "tipo": str(question.get("tipo", "")),
        "estado": bool(question.get("estado", False))
    }

def schema_request(request: Dict) -> Dict:
    """Valida los datos de entrada y los convierte a un diccionario limpio."""
    return {
        "pregunta": str(request.get("pregunta", "")),
        "opciones": list(request.get("opciones", [])),
        "respuesta_correcta": str(request.get("respuesta_correcta", "")),
        "nivel"  : str(request.get("nivel", "")),
        "categoria": category_question_schema(request.get("categoria", {})),
    }

def many_question_schema(questions)->list:
    return [question_schema(question) for question in questions]

def many_request_schema(requests)->list:
    return [schema_request(request) for request in requests]