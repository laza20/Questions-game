from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status
from db.client import db_client
from typing import get_type_hints


def validate_object_id(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")
    
def validate_object_id_or_false(id: str):
    try:
        return ObjectId(id)
    except InvalidId:
        return False
    
def buscar_data(id, base_de_datos_2):
    coleccion = getattr(db_client, base_de_datos_2)
    oid = validate_object_id(id)
    data = coleccion.find_one({"_id":oid})
    if not data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Dato incorrecta")
    
    return data


def usar_coleccion(base_de_datos):
    coleccion = getattr(db_client, base_de_datos)
    return coleccion