from utils import funcion_nivel_pregunta
import re
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.questions import Question
from db.client import db_client
from utils import db_helpers, funciones_logicas, funciones_randoms, graphlookups
from exceptions import errores_simples
import random


def insertar_question(preguntas: List[Question]) -> List[Dict]:
    """
    Función principal para validar e insertar una o varias preguntas.
    """
    if not isinstance(preguntas, list) or not preguntas:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se espera una lista de preguntas.")
        
    documentos_a_insertar = []
    
    # Conjunto para detectar duplicados en la carga masiva
    preguntas_cargadas = set()

    for pregunta in preguntas:
        # 1. Validación de negocio. Llamamos a las validaciones privadas y unificadas.
        pregunta.nivel = _validate_question(pregunta)
        
        # 2. Verificar duplicados en la carga masiva
        key = _create_key(pregunta)
        if key in preguntas_cargadas:
            errores_simples.error_carga_repetida_un_solo_dato(pregunta.pregunta, "Preguntas")
            
        preguntas_cargadas.add(key)
        
        
        # 3. Preparación del documento
        documento = pregunta.model_dump(by_alias=True, exclude_none=True)
        
        documento["categoria_id"] = db_helpers.get_categoria_id(pregunta.categoria_id)
        documento.pop("id", None)
        documentos_a_insertar.append(documento)
        
    coleccion = db_client.Preguntas
    if len(documentos_a_insertar) == 1:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        nuevos_documentos = [coleccion.find_one({"_id": id})]
    else:
        resultado = coleccion.insert_many(documentos_a_insertar)
        nuevos_documentos = list(coleccion.find({"_id": {"$in": resultado.inserted_ids}}))
        
    documentos = [_format_document(doc) for doc in nuevos_documentos]
            
    return documentos

def visionar_todas_las_preguntas()-> List[Dict]:
    documentos = list(db_client.Preguntas.find({"tipo":"Preguntas"}))
    if not documentos:
        _sin_preguntas()
    
    documentos_formateados = [_format_document(doc) for doc in documentos]
    return documentos_formateados


def modificar_id():
    documentos = list(db_client.Preguntas.find({"tipo":"Preguntas"}))
    if not documentos:
        _sin_preguntas()
    
    lista_documentos = []
    
    for documento in documentos:
        categoria_id = documento.get("categoria_id")
        id = documento.get("_id")
        if not categoria_id:
            continue
        
        documento["categoria_id"] = funciones_logicas.validate_object_id(documento["categoria_id"])
        db_client.Preguntas.replace_one({"_id":id}, documento)
        lista_documentos.append(documento)
        
    if lista_documentos:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Lista actualizada correctamente")
    else:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error al modificar los oid")
        
        
def play_question_random() -> Dict:
    """
    Función que selecciona una pregunta aleatoria de forma eficiente,
    con un número limitado de intentos.
    """
    intentos_maximos = 10
    intentos = 0

    while intentos < intentos_maximos:
        # 1. Elegir un nivel y categoría de forma aleatoria.
        nivel_elegido = funciones_randoms.aleatorizar_niveles()
        categoria_elegida = funciones_randoms.aleatorizar_categorias_generales()

        try:
            # 2. Llamar a la nueva función para obtener documentos
            documentos = db_helpers.seleccionar_pregunta_con_graphlookup(categoria_elegida, nivel_elegido)
        except HTTPException:
            # Si la categoría no existe, se incrementa el contador y se intenta de nuevo
            intentos += 1
            continue

        # Si se encuentra un documento, se sale del bucle y se retorna
        if documentos:
            pregunta_elegida = documentos[0]
            # No se necesita modificar categoria_id aquí, ya que el documento devuelto
            # por la pipeline ya es correcto.
            return _format_document(pregunta_elegida)
        
        intentos += 1

    # Si se superan los intentos sin encontrar un documento, se lanza una excepción
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se pudo encontrar una pregunta aleatoria después de varios intentos. Inténtelo de nuevo más tarde."
    )
    
def play_question_by_category(categoria:str) -> Dict:
    """
    Función que selecciona una pregunta aleatoria de una categoria determinada.
    """
    intentos_maximos = 10
    intentos = 0

    while intentos < intentos_maximos:
        # 1. Elegir un nivel y categoría de forma aleatoria.
        nivel_elegido = funciones_randoms.aleatorizar_niveles()
        try:
            # 2. Llamar a la nueva función para obtener documentos
            documentos = db_helpers.seleccionar_pregunta_con_graphlookup(categoria, nivel_elegido)
        except HTTPException:
            # Si la categoría no existe, se incrementa el contador y se intenta de nuevo
            intentos += 1
            continue

        # Si se encuentra un documento, se sale del bucle y se retorna
        if documentos:
            pregunta_elegida = documentos[0]
            # No se necesita modificar categoria_id aquí, ya que el documento devuelto
            # por la pipeline ya es correcto.
            return _format_document(pregunta_elegida)
        
        intentos += 1

    # Si se superan los intentos sin encontrar un documento, se lanza una excepción
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se pudo encontrar una pregunta aleatoria después de varios intentos. Inténtelo de nuevo más tarde."
    )

def _validate_question(dato: Question):
    """Funcion orquestadora de validaciones"""
    
    _verificar_respuesta_correcta(dato)
    _verificar_pregunta_unica(dato.pregunta)

    if dato.puntos_pregunta:
        nivel = funcion_nivel_pregunta.cargar_nivel_pregunta(dato.puntos_pregunta)
        dato.nivel = nivel
    
    return dato.nivel

        
def _verificar_respuesta_correcta(dato: Question):
    """Funcion que verifica que la respuesta correcta esta entre las opciones proporcionadas."""
    if dato.respuesta_correcta not in dato.opciones:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La respuesta correcta: '{dato.respuesta_correcta}' no se encuentra entre las opciones {dato.opciones}"
        )
        
def _verificar_pregunta_unica(pregunta_str: str):
    """Funcion que verifica que la pregunta no se encuentre ya guardada en la base de datos."""
    pattern = f"^{re.escape(pregunta_str.strip())}$"
    if db_client.Preguntas.find_one({"pregunta": {"$regex": pattern, "$options": "i"}}):
        errores_simples.error_simple_positivo(pattern, "Preguntas", "pregunta")




def _create_key(dato: Question):
    """Funcion que retorna el valor que se va a guardar en el conjunto para verificar
    que no haya carga repetida."""
    return dato.pregunta.strip().lower()


def _format_document(doc: Dict) -> Dict:
    """Funcion que formatea el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        doc["categoria_id"] = str(doc["categoria_id"])
    return doc

def _sin_preguntas():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontraron las preguntas necesarias"
        )






    