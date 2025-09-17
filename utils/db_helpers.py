from bson.objectid import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from typing import Dict, List
from utils import funciones_logicas, graphlookups, funcion_nivel_pregunta


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
        print(documento)
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

def get_id_category(nombre):
    categoria = db_client.Categorias.find_one({"nombre":nombre})
    id_categoria = categoria["_id"]
    return id_categoria
    
    
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


def identificar_categoria_con_graphlookup(categoria_id: str):
    """
    Función para identificar la categoría principal de una pregunta
    buscando en la jerarquía de categorías.
    """
    try:
        # Step 2: Find the category to check if it exists
        categoria_actual = db_client.Categorias.find_one({"_id": categoria_id})

        if not categoria_actual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La categoría con ID '{categoria_id}' no existe."
            )

        # Step 3: Check if the category is already a top-level parent
        if categoria_actual.get("padre_id") is None:
            return categoria_actual

        # Step 4: If it has a parent, use graphLookup to find the ultimate ancestor
        # The get_main_category function already handles the entire hierarchy traversal
        categoria_principal = graphlookups.get_main_category(categoria_id)
        
        if not categoria_principal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la categoría principal para el ID '{categoria_id}'."
            )
            
        print(f"Categoría principal encontrada: {categoria_principal['nombre']}")
        return categoria_principal
        
    except HTTPException as e:
        # Re-raise the HTTPException
        raise e
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado: {e}"
        )
        
        
def identificar_categorias_descentes_con_graphlookup(categoria_id: str):
    """
    Función para identificar las categoría inferiores de una pregunta
    buscando en la jerarquía de categorías.
    """
    try:
        categoria_object_id = ObjectId(categoria_id)
        categoria_actual = db_client.Categorias.find_one({"_id": categoria_object_id})

        if not categoria_actual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La categoría con ID '{categoria_id}' no existe."
            )
        descendant_docs = graphlookups.get_all_descendants(categoria_id)

        descendant_ids = {doc["_id"] for doc in descendant_docs}
        
        descendant_ids.add(categoria_object_id)

        return descendant_ids
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado: {e}"
        )
        
def asignacion_de_puntos_a_pregunta(pregunta_elegida, respuesta):
    puntos = pregunta_elegida["puntos_pregunta"]
    if pregunta_elegida["respuesta_correcta"] == respuesta["respuesta_correcta"]:
        
        if pregunta_elegida["consecutiva"] <= 0:
            pregunta_elegida["puntos_pregunta"] -= 10
            pregunta_elegida["consecutiva"] = 0
            pregunta_elegida["consecutiva"] += 1
            pregunta_elegida["nivel"] = funcion_nivel_pregunta.cargar_nivel_pregunta(puntos)
        else: 
            pregunta_elegida["puntos_pregunta"] -= 20
            pregunta_elegida["consecutiva"] += 1
            pregunta_elegida["nivel"] = funcion_nivel_pregunta.cargar_nivel_pregunta(puntos)
        
        respuesta_acertada = "CORRECTA"
        
        
    if pregunta_elegida["respuesta_correcta"] != respuesta["respuesta_correcta"]:
        if pregunta_elegida["consecutiva"] >= 0:
            pregunta_elegida["puntos_pregunta"] += 10
            pregunta_elegida["consecutiva"] = 0
            pregunta_elegida["consecutiva"] -= 1
            pregunta_elegida["nivel"] = funcion_nivel_pregunta.cargar_nivel_pregunta(puntos)
        else:
            pregunta_elegida["puntos_pregunta"] += 20
            pregunta_elegida["consecutiva"] -= 1
            pregunta_elegida["nivel"] = funcion_nivel_pregunta.cargar_nivel_pregunta(puntos)
        
        respuesta_acertada = "INCORRECTA"
        
    return pregunta_elegida, respuesta_acertada

def sin_usuario():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontrar al usuario necesario."
        )