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

def get_main_category(subcategory_id: str):
    """
    Funcion encargada de buscar la categoria principal de una categoria inferior."
    """
    try:
        # 1. Validate the input ID
        category_object_id = ObjectId(subcategory_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category ID.")

    # 2. Use $graphLookup to get the entire ancestry path
    pipeline = [
        {"$match": {"_id": category_object_id}},
        {"$graphLookup": {
            "from": "Categorias",
            "startWith": "$padre_id",
            "connectFromField": "padre_id",
            "connectToField": "_id",
            "as": "ancestry_path",
            "maxDepth": 10
        }}
    ]
    
    result = list(db_client.Categorias.aggregate(pipeline))

    if not result:
        # This means the initial category was not found
        return None

    # The result should contain the starting document and the ancestry path
    ancestry_path = result[0].get("ancestry_path", [])

    # If the ancestry path is empty, it means the category is already a top-level parent
    if not ancestry_path:
        return result[0]
        
    # The last element in the ancestry path is the main category
    main_category = ancestry_path[-1]

    return main_category


