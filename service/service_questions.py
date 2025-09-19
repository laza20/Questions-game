from utils import funcion_nivel_pregunta
from datetime import datetime, timezone
import re
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.questions import Question
from service import service_conexion_logros
from db.client import db_client
from utils import (
    db_helpers, 
    funciones_logicas, 
    funciones_randoms, 
    graphlookups, 
    funcion_nivel_pregunta,
    funcion_niveles_usuario,
    puntos_usuario_por_pregunta
    )
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
            pregunta_elegida["categoria_id"] = db_helpers.get_categoria_id(pregunta_elegida["categoria_id"])
            pregunta_elegida["categoria_id"] = db_helpers.get_name_category(pregunta_elegida["categoria_id"])
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
            pregunta_elegida["categoria_id"] = db_helpers.get_categoria_id(pregunta_elegida["categoria_id"])
            pregunta_elegida["categoria_id"] = db_helpers.get_name_category(pregunta_elegida["categoria_id"])
            # No se necesita modificar categoria_id aquí, ya que el documento devuelto
            # por la pipeline ya es correcto.
            return _format_document(pregunta_elegida)
        
        intentos += 1

    # Si se superan los intentos sin encontrar un documento, se lanza una excepción
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se pudo encontrar una pregunta aleatoria después de varios intentos. Inténtelo de nuevo más tarde."
    )
    
def play_duel() -> Dict:
    """
    Función que selecciona 10 preguntas aleatorias para un duelo.
    """
    intentos_maximos = 100
    intentos = 0
    preguntas = []
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
            pregunta_elegida["categoria_id"] = db_helpers.get_categoria_id(pregunta_elegida["categoria_id"])
            pregunta_elegida["categoria_id"] = db_helpers.get_name_category(pregunta_elegida["categoria_id"])
            pregunta_formateada = _format_document(documentos[0])
            
            if pregunta_elegida in preguntas:
                intentos += 1
            else:
                preguntas.append(pregunta_formateada)
            # No se necesita modificar categoria_id aquí, ya que el documento devuelto
            # por la pipeline ya es correcto.
            if len(preguntas) == 10:
                return preguntas
        
        intentos += 1

    # Si se superan los intentos sin encontrar un documento, se lanza una excepción
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se pudo encontrar una pregunta aleatoria después de varios intentos. Inténtelo de nuevo más tarde."
    )
    
def play_duel_category(categoria:str) -> Dict:
    """
    Función que selecciona 10 preguntas aleatorias para un duelo.
    """
    intentos_maximos = 100
    intentos = 0
    preguntas = []
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
            pregunta_elegida["categoria_id"] = categoria.capitalize()
            pregunta_formateada = _format_document(documentos[0])
            
            if pregunta_elegida in preguntas:
                intentos += 1
            else:
                preguntas.append(pregunta_formateada)
            # No se necesita modificar categoria_id aquí, ya que el documento devuelto
            # por la pipeline ya es correcto.
            if len(preguntas) == 10:
                return preguntas
        
        intentos += 1

    # Si se superan los intentos sin encontrar un documento, se lanza una excepción
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se pudo encontrar una pregunta aleatoria después de varios intentos. Inténtelo de nuevo más tarde."
    )
    
    
def aswer_one_question(respuesta:dict, current_user:dict) -> Dict:
    """
    Funcion que sirve para responder una pregunta
    """
    id_respuesta = respuesta["id"]
    oid_respuesta = funciones_logicas.validate_object_id(id_respuesta)
    pregunta_elegida = db_client.Preguntas.find_one({"_id":oid_respuesta})
    pregunta_elegida["categoria_id"] = db_helpers.get_categoria_id(pregunta_elegida["categoria_id"])
    pregunta_elegida["categoria_id"] = db_helpers.get_name_category(pregunta_elegida["categoria_id"])
    
 
    pregunta_elegida, respuesta_acertada = db_helpers.asignar_puntos_y_nivel(pregunta_elegida, respuesta)
    
        
    db_client.Preguntas.find_one_and_replace({"_id":oid_respuesta}, pregunta_elegida)
    nivel_pregunta = pregunta_elegida["nivel"]
    puntos_positivos, puntos_negativos = puntos_usuario_por_pregunta.puntos_por_nivel_pregunta(nivel_pregunta)
    if respuesta_acertada == "CORRECTA":
        _actualizar_progreso(pregunta_elegida, current_user, nivel_pregunta)
        puntos_a_sumar = puntos_positivos 
        nivel = funcion_niveles_usuario.niveles_usuario(current_user["stats"]["puntos_xp"])
        updates = {
            "$inc": {"stats.puntos_xp": puntos_a_sumar},
            "$set": {"stats.nivel": nivel}
        }
    elif respuesta_acertada == "INCORRECTA" and current_user["stats"]["puntos_xp"] <= 1700 and current_user["stats"]["nivel"] >= 15:
        updates = {
            "$inc": {"stats.puntos_xp": puntos_negativos},
        }
    else:
        updates = {} 

    if updates:
        usuario_modificado = db_client.Usuarios.find_one_and_update(
            {"_id": current_user["_id"]},
            updates,
            return_document=True 
        )
    else:
        usuario_modificado = db_client.Usuarios.find_one({"_id": current_user["_id"]})
        
    if respuesta_acertada == "CORRECTA":
        puntos = puntos_positivos
    else:
        puntos = puntos_negativos
        
    dict_pregunta_respondida = _conformar_dict_preg_respondida(current_user, pregunta_elegida, respuesta, respuesta_acertada, puntos)
    
    db_client.Preguntas_respondidas.insert_one(dict_pregunta_respondida).inserted_id
    usuario_formateado = db_helpers.transformar_id(usuario_modificado)
    pregunta_formateada = _format_document(pregunta_elegida)
    pregunta_formateada["respuesta_acertada"] = respuesta_acertada
        
    service_conexion_logros.orquestador_logros(current_user, "pregunta_respondida", pregunta_formateada)

    return pregunta_formateada, usuario_formateado

def view_question_for_id(id:str) -> Dict:
    """
    Funcion que sirve para visualizar una pregunta por medio del id
    """
    oid = funciones_logicas.validate_object_id(id)
    pregunta = db_client.Preguntas.find_one({"_id":oid})
    if not pregunta:
        _sin_preguntas()
    pregunta_formateada = _format_document(pregunta)
    return pregunta_formateada

def _validate_question(dato: Question):
    """Funcion orquestadora de validaciones"""
    
    _verificar_respuesta_correcta(dato)
    _verificar_pregunta_unica(dato.pregunta)

    if dato.puntos_pregunta:
        nivel = funcion_nivel_pregunta.cargar_nivel_pregunta(dato.puntos_pregunta)
        dato.nivel = nivel
    
    return dato.nivel

def _actualizar_progreso(pregunta, current_user, nivel_pregunta):
    id_categoria = db_helpers.get_categoria_id(pregunta["categoria_id"])
    categoria_principal = db_helpers.identificar_categoria_con_graphlookup(id_categoria)
    nombre_categoria = categoria_principal["nombre"]
    
    updates = {}
    updates["progreso.preguntas_correctas"] = 1
    
    dificultad_map = {
        "Muy facil": "preguntas_muy_faciles_correctas",
        "Facil": "preguntas_faciles_correctas",
        "Medio": "preguntas_medio_correctas",
        "Dificil": "preguntas_dificil_correctas",
        "Imposible": "preguntas_imposible_correctas",
        "Infinito": "preguntas_infinito_correctas"
    }
    campo_dificultad = dificultad_map.get(nivel_pregunta)
    if campo_dificultad:
        updates[f"progreso.{campo_dificultad}"] = 1

    categoria_map = {
        "Entretenimiento": "preguntas_entretenimiento_correctas",
        "ciencia": "preguntas_ciencia_correctas",
        "historia": "preguntas_historia_correctas",
        "cultura general": "preguntas_cultura_general_correctas",
        "deportes": "preguntas_deportes_correctas"
    }
    campo_categoria = categoria_map.get(nombre_categoria)
    if campo_categoria:
        updates[f"progreso.{campo_categoria}"] = 1
        
    db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$inc": updates}
    )


def _conformar_dict_preg_respondida(current_user, pregunta_elegida, respuesta, respuesta_acertada, puntos):
    dict_pregunta_respondida = {}
    dict_pregunta_respondida = {"id_usuario":current_user["_id"],
        "id_pregunta"           : pregunta_elegida["_id"],
        "respuesta_del_usuario" : respuesta["respuesta_correcta"],
        "respuesta"             : respuesta_acertada,
        "puntos_obtenidos"      : puntos,
        "timestamp" : datetime.now(timezone.utc)}
    return dict_pregunta_respondida
        
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






    