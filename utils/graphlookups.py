from db.client import db_client
from bson.objectid import ObjectId
from fastapi import HTTPException, status
from utils import db_helpers, funciones_randoms


#Busqueda de ids desde categoria principal
def get_all_descendant_ids_principal(parent_id: ObjectId) -> list[ObjectId]:
    """
    Funcion encargada de retornar los ids de rangos inferiores por medio del padre id.
    """
    pipeline = [
        {
            "$match": {"_id": parent_id} #punto de partida
        },
        {
            "$graphLookup": {
                "from": "Categorias", # coleccion
                "startWith": "$_id", # dato a buscar
                "connectFromField": "_id", # dato por el que esta conectado
                "connectToField": "padre_id",# lugar donde se va a buscar el dato
                "as": "subcategories" # nombre del array
            }
        },
        {
            "$project": {
                "all_ids": {
                    "$concatArrays": [["$_id"], "$subcategories._id"] # Creacion de un array que contenga el id padre e hijo
                }
            }
        }
    ]

    result = list(db_client.Categorias.aggregate(pipeline)) # Agrega los los ids a una lista
    return result[0]['all_ids'] if result else [parent_id] # retorna los ids para utilizarlos en el match
    
    
#Busqueda de ids desde categoria principal
def get_all_descendant_ids_second_level(parent_id: ObjectId) -> list[ObjectId]:
    """
    Funcion encargada de retornar los ids de rangos inferiores al segundo nivel por medio del padre id.
    """
    pipeline = [
        {
            "$match": {
                "padre_id": parent_id,
                "grado": "Segundo"
            }
        },
        {
            "$graphLookup": {
                "from": "Categorias",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "padre_id",
                "as": "subcategories"
            }
        },
        {
            "$project": {
                "all_ids": {
                    "$concatArrays": [["$_id"], "$subcategories._id"]
                }
            }
        }
    ]

    result = list(db_client.Categorias.aggregate(pipeline)) # Agrega los los ids a una lista
    return result[0]['all_ids'] if result else [parent_id] # retorna los ids para utilizarlos en el match


