# In services/categorias_service.py
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.categorias import Categoria
from db.client import db_client
from bson.objectid import ObjectId
from typing import Optional
from validaciones_generales import validaciones_simples
from exceptions import errores_simples

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
        _verificar_grado_categoria(categoria)
        _validaciones_categoria(categoria)
        
        # 2. Verificar duplicados en la carga masiva
        key = _create_key(categoria)
        if key in nombres_cargados:
            errores_simples.error_carga_repetida_un_solo_dato(categoria.nombre, "Categorias")
            
        nombres_cargados.add(key)
        
        # 3. Preparación del documento
        documento = categoria.model_dump(by_alias=True, exclude_none=True)
        del documento["id"]
        documento["tipo"] = "Categoria"
        documentos_a_insertar.append(documento)
        
    # Inserción en la base de datos
    coleccion = db_client.Categorias
    if len(documentos_a_insertar) == 1:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        nuevos_documentos = [coleccion.find_one({"_id": id})]
    else:
        resultado = coleccion.insert_many(documentos_a_insertar)
        nuevos_documentos = list(coleccion.find({"_id": {"$in": resultado.inserted_ids}}))
        
    documentos = [serializar_doc(doc) for doc in nuevos_documentos]
            
    return documentos


def serializar_doc(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# --- Funciones de validación privadas, ahora unificadas aquí ---

def _verificar_grado_categoria(categoria: Categoria):
    if categoria.grado == "Primer":
        _verificar_limite_categoria_principal()
    else:
        try:
            oid_padre = ObjectId(categoria.padre_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El ID de la categoría padre no es válido: {categoria.padre_id}"
            )
        if not db_client.Categorias.find_one({"_id": oid_padre}):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontró la categoría padre con el ID: {categoria.padre_id}"
            )

def _verificar_limite_categoria_principal():
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
    if dato.grado == "Primer":
        return dato.nombre.lower()
    else:
        return (dato.nombre.lower(), oid_padre)