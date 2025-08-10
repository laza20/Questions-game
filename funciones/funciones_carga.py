from bson import ObjectId
from fastapi import HTTPException, status
from db.client import db_client
from funciones import funciones_logicas
    
#Funcion para agrupar el codigo repetido, permite cumplir con una responsabilidad unica por funcion. Armar el dict.    
def logica_de_carga_normal(dato, base_de_datos):
        dict_dato = dict(dato)
        dict_dato["tipo"] = base_de_datos
        return dict_dato
    
def cargar_uno(dato, base_de_datos, schema, validacion):
        coleccion = getattr(db_client, base_de_datos)
        validacion(dato, base_de_datos)
        dict_dato = logica_de_carga_normal(dato, base_de_datos)
        id = coleccion.insert_one(dict_dato).inserted_id
        new_formato = schema(coleccion.find_one({"_id":id}))
        return new_formato
    
    
#Funcion para cargar un muchos documentos que no sean circuito_por_temporada, piloto_por_temporada, Equipo_por_temporada.
def cargar_muchos(datos, base_de_datos , schema, validacion):
    coleccion = getattr(db_client, base_de_datos)
    lista = []
    validacion(datos, base_de_datos)
    for dato in datos:
        dict_dato = logica_de_carga_normal(dato, base_de_datos)
        lista.append(dict_dato)
        
    resultado = coleccion.insert_many(lista)
    ids = resultado.inserted_ids
    documentos = coleccion.find({"_id":{"$in":ids}})
    return schema(documentos) 