from bson import ObjectId
from fastapi import HTTPException, status
from typing import List, Optional, Union
from db.client import db_client
from db.models.questions import QuestionRequest
from db.models.questions import Question as QuestionDB
from db.schemas.questions import question_schema, schema_request
from datetime import datetime
from service import service_questions
from utils import funcion_nivel_pregunta


def cargar_documentos(datos, base_de_datos, validacion):
    """
    Función genérica para cargar uno o varios documentos.
    """
    coleccion = getattr(db_client, base_de_datos)
    es_lista = isinstance(datos, list)
    lista_documentos = datos if es_lista else [datos]
    
    documentos_a_insertar = []
    for dato in lista_documentos:
        
        dict_dato = dato.model_dump()
        
        # Agregamos los campos del sistema
        dict_dato = verificar_puntos_preg(dato, dict_dato)
        nivel = funcion_nivel_pregunta.cargar_nivel_pregunta(dict_dato["puntos_pregunta"])
        dict_dato = conformar_dict(dict_dato, nivel, base_de_datos)
        documentos_a_insertar.append(dict_dato)
        
    validacion(lista_documentos, base_de_datos)
    # Insertamos en la base de datos de forma eficiente
    if es_lista:
        resultado = coleccion.insert_many(documentos_a_insertar)
        documentos_insertados = coleccion.find({"_id": {"$in": resultado.inserted_ids}})
        return [schema_request(doc) for doc in documentos_insertados]
    else:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        documentos_insertados = coleccion.find_one({"_id": id})
        return schema_request(documentos_insertados)
    
    
def verificar_puntos_preg(dato, dict_dato):
    if dato.puntos_pregunta != None:
        dict_dato.update({
            "puntos_pregunta": dato.puntos_pregunta
        })
    else:
        dict_dato.update({
            "puntos_pregunta": 500
        })
    
    return dict_dato


def conformar_dict(dict_dato, nivel, base_de_datos):
    dict_dato.update({
        "nivel" : nivel,
        "consecutiva":0,
        "usuario_carga": "Master", 
        "fecha_carga": datetime.now(),
        "tipo" : base_de_datos,
        "estado": True
    })
    del dict_dato["id"]
    return dict_dato