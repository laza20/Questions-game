from bson.objectid import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from typing import Dict, List
from utils import funciones_logicas


def get_categoria_id(referencia_categoria: str):
    """
    Función unificada para encontrar un ID de categoría.
    Acepta tanto un ObjectId válido como un nombre de categoría.
    """
    try:
        # Intenta convertir la referencia en un ObjectId.
        oid = ObjectId(referencia_categoria)
        # Si tiene éxito, busca por ID.
        documento = db_client.Categorias.find_one({"_id": oid})
        if not documento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la categoría con el ID: {referencia_categoria}"
            )
        return oid
    except Exception:
        documentos = list(db_client.Categorias.find({"nombre":{"$regex": f"^{referencia_categoria}$", "$options": "i"}}))
        if not documentos:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la categoría con el nombre: {referencia_categoria}"
            )
        if len(documentos) > 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El nombre '{referencia_categoria}' corresponde a varias categorías. Por favor, use el ID en su lugar."
            )
        
        # Si se encuentra un solo documento por nombre, retorna su ID.
        padre_oid = funciones_logicas.validate_object_id(documentos[0]['_id'])
        return padre_oid
    
    
    
def transformar_id(doc: Dict) -> Dict:
    """Funcion encargada de formatear el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

def seleccionar_pregunta(categoria_elegida, nivel_elegido):
    """Funcion encargada de buscar una pregunta de un nivel y categoria determinada."""
    categoria_id = get_categoria_id(categoria_elegida)

    # 3. Realizar la consulta a la base de datos.
    coleccion = db_client.Preguntas
    pipeline = [
        {
            "$match": {
                "categoria_id": categoria_id,
                "nivel": {"$regex": f"^{nivel_elegido}$", "$options": "i"}
            }
        },
        {"$sample": {"size": 1}}
    ]
    documentos = list(coleccion.aggregate(pipeline))
    return documentos
        