# In services/categorias_service.py
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.categorias import Categoria
from db.client import db_client
from bson.objectid import ObjectId
from utils import db_helpers, funciones_logicas
from typing import Optional
from validaciones_generales import validaciones_simples
from exceptions import errores_simples



def iniciar_duelo(current_user:dict) -> Dict:
    duelo = {"usuario_uno_id": current_user["_id"],
             }
    
    id = db_client.Duelos.insert_one(duelo).inserted_id
    nuevo_duelo = db_client.Duelos.find_one({"_id": id})
    duelo_transformado = _transformar_id(nuevo_duelo)
    return duelo_transformado
    
    
    
def _transformar_id(doc: Dict) -> Dict:
    """Funcion encargada de formatear el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        doc["usuario_uno_id"] = str(doc["usuario_uno_id"])
    return doc