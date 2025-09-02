from bson.objectid import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from typing import Dict, List
from utils import funciones_logicas, graphlookups


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
    
def get_name_category(oid):
    categoria = db_client.Categorias.find_one({"_id":oid})
    nombre_categoria = categoria["nombre"]
    return nombre_categoria
    
    
def transformar_id(doc: Dict) -> Dict:
    """Funcion encargada de formatear el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

def seleccionar_pregunta_con_graphlookup(categoria_elegida: str, nivel_elegido: str):
    """
    Function that finds a question in a category and its subcategories.
    """
    try:
        # 1. Get the _id of the main category.
        categoria_padre_id = get_categoria_id(categoria_elegida)
        
        # 2. Get all the IDs from the main category's tree.
        all_relevant_ids = graphlookups.get_all_descendant_ids_principal(categoria_padre_id)
        
    except HTTPException:
        # Raises an exception if the category is not found.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La categoría '{categoria_elegida}' no existe."
        )

    # 3. Perform a simple and efficient search with the obtained IDs.
    coleccion = db_client.Preguntas
    pipeline = [
        {
            "$match": {
                "categoria_id": {"$in": all_relevant_ids}, # Busca la docts. de los ids que encontro anteriormente
                "nivel": {"$regex": f"^{nivel_elegido}$", "$options": "i"} # con este nivel 
            }
        },
        {"$sample": {"size": 1}} # Elige una de manera aleatoria.
    ]
    documentos = list(coleccion.aggregate(pipeline))
    return documentos
        