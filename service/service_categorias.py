# In services/categorias_service.py
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.categorias import Categoria
from db.client import db_client
from bson.objectid import ObjectId
from utils import db_helpers
from typing import Optional
from validaciones_generales import validaciones_simples
from exceptions import errores_simples

"""Inicio de llamadas al usuario """
def insertar_categorias(categorias: List[Categoria]) -> List[Dict]:
    """
    Función principal para validar e insertar una o varias categorías.
    """
    if not isinstance(categorias, list) or not categorias:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se espera una lista de categorías.")
        
    documentos_a_insertar = []
    
    # Conjunto para detectar duplicados en la carga masiva
    nombres_cargados = set()

    for categoria in categorias:
        # 1. Validación de negocio. Llamamos a las validaciones privadas y unificadas.
        if categoria.grado == "Primer":
            _verificar_limite_categoria_principal()
            
        oid_padre = None
        if categoria.grado != "Primer" and categoria.padre_id:
                    oid_padre = db_helpers.get_categoria_id(categoria.padre_id)
        
        # 2. Verificar duplicados en la carga masiva
        key = _create_key(categoria, oid_padre)
        if key in nombres_cargados:
            errores_simples.error_carga_repetida_un_solo_dato(categoria.nombre, "Categorias")
        nombres_cargados.add(key)
            
        nombres_cargados.add(key)
        
        # 3. Preparación del documento
        documento = categoria.model_dump(by_alias=True, exclude_none=True)
        del documento["id"]
        documento["tipo"] = "Categoria"
        documento["padre_id"] = db_helpers._get_categoria_id(categoria.padre_id)
        documentos_a_insertar.append(documento)
        
    # Inserción en la base de datos
    coleccion = db_client.Categorias
    if len(documentos_a_insertar) == 1:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        nuevos_documentos = [coleccion.find_one({"_id": id})]
    else:
        resultado = coleccion.insert_many(documentos_a_insertar)
        nuevos_documentos = list(coleccion.find({"_id": {"$in": resultado.inserted_ids}}))
        
    documentos = [_format_document(doc) for doc in nuevos_documentos]
            
    return documentos


def visionar_todas_las_categorias()-> List[Dict]:
    documentos = list(db_client.Categorias.find({"tipo":"Categoria"}))
    if not documentos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"No se encontraron las categorias necesarias"
            )
    
    documentos_formateados = [_format_document(doc) for doc in documentos]
    return documentos_formateados


def visionar_categorias_por_nivel(grado:str)-> List[Dict]:
    documentos = list(db_client.Categorias.find({"grado":{"$regex": f"^{grado}$", "$options": "i"}}))
    if not documentos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"No se encontraron las categorias necesarias"
            )
    
    documentos_formatedos = [_format_document(doc) for doc in documentos]
    return documentos_formatedos


""" Fin de llamadas al usuario """


""" Funciones privadas de este archivo """

def _verificar_limite_categoria_principal():
    """Funcion encargada de verificar si una categoria es principal y en 
    caso de serlo verifica que no haya mas de 5 de este grado."""
    cantidad = db_client.Categorias.count_documents({"grado": "Primer"})
    if cantidad >= 5:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Se ha alcanzado el límite de 5 categorías principales."
        )

def _validaciones_categoria(dato: Categoria, oid_padre: Optional[ObjectId] = None):
    validaciones_simples.validacion_simple_general("Categorias", dato.nombre)
    validaciones_simples.validacion_simple_general("Categorias", dato.descripcion)
    if oid_padre:
        validaciones_simples.validacion_simple_general_negativa("Categorias", oid_padre)

def _create_key(dato: Categoria, oid_padre: Optional[ObjectId] = None):
    """Funcion encargada de generar una key la cual permite verificar que los documentos
    ingresados no se repitan."""
    if dato.grado == "Primer":
        return dato.nombre.lower()
    else:
        return (dato.nombre.lower(), str(oid_padre))
    
def _format_document(doc: Dict) -> Dict:
    """Funcion que formatea el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        if "padre_id" in doc and doc["padre_id"] is not None:
            doc["padre_id"] = str(doc["padre_id"])
    return doc
