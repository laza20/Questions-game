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
    Funcion encargada de buscar una pregunta de una categoria padre en sus hijos 
    y retornar la pregunta final.
    """
    try:
        # Obtiene el padre id por medio del nombre
        categoria_padre_id = get_categoria_id(categoria_elegida)
        
        # Obtiene todos los ids de las sub categorias de una categoria padre
        all_relevant_ids = graphlookups.get_all_descendant_ids_principal(categoria_padre_id)
        
    except HTTPException:
        # En caso de que la categoria ingresada no exista en la base de datos.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La categoría '{categoria_elegida}' no existe."
        )

    # Busqueda de documentos que cumplan con las condiciones planteadas.
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
        