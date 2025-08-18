# pyright: reportInvalidTypeForm=false
from funciones import funciones_carga, funcion_carga_questions
from db.client import db_client
from fastapi import status, Body
from pydantic import BaseModel
from typing import Type, Any, List
from db.models.questions import QuestionRequest, Question
from funciones import funcion_nivel_pregunta, funciones_logicas
from db.schemas.questions import many_request_schema

def agregar_puntos(router, base_de_datos, schema):
    @router.put("/Inicializar/Puntos", response_model = list[QuestionRequest], status_code=status.HTTP_202_ACCEPTED)
    async def restart_points():
        coleccion = getattr(db_client, base_de_datos)
        lista_documentos = []
        dict_documento   = {}
        documentos = schema(coleccion.find({"tipo":base_de_datos}))
        for documento in documentos:
            dict_documento = documento
            dict_documento["puntos_pregunta"] = 500
            dict_documento["nivel"]  = funcion_nivel_pregunta.cargar_nivel_pregunta(dict_documento["puntos_pregunta"])
            dict_documento["consecutiva"] = 0
            id = dict_documento["id"]
            oid = funciones_logicas.validate_object_id(id)
            coleccion.find_one_and_replace({"_id":oid}, dict_documento)
            lista_documentos.append(dict_documento)
            
            
        return many_request_schema(lista_documentos)
    
    
def modificar_puntos_by_id(router, base_de_datos, schema):
    @router.put("/Modificar/Por/{id}/{puntos}", response_model = Question, status_code=status.HTTP_202_ACCEPTED)
    async def replace_by_id(id:str, puntos:int):
        coleccion = getattr(db_client, base_de_datos)
        dict_documento = {}
        oid = funciones_logicas.validate_object_id(id)
        dict_documento = coleccion.find_one({"_id":oid})
        dict_documento["puntos_pregunta"] = puntos
        dict_documento["nivel"]  = funcion_nivel_pregunta.cargar_nivel_pregunta(dict_documento["puntos_pregunta"])
        coleccion.find_one_and_replace({"_id":oid}, dict_documento)
        
        return schema(dict_documento)
            