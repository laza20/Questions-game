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
from datetime import datetime, timezone
import random


def iniciar_duelo(current_user:dict) -> Dict:
    
    duelos_actuales = list(db_client.Duelos.find({"usuario_dos_id":None}))
    
    if len(duelos_actuales) >= 1:
        duelo_elegido = random.choice(duelos_actuales)
        duelo_elegido["usuario_dos_id"] = current_user["_id"]
        
        update_changes = {
            "$set": {
                "usuario_dos_id": duelo_elegido["usuario_dos_id"],
                "numero_de_ronda": 1, 
                }
        }
        
        db_client.Duelos.update_one(
            {"_id": duelo_elegido["_id"]}, 
            update_changes
        )
        
        mostrar_duelo = db_client.Duelos.find_one({"_id":duelo_elegido["_id"]})
        
        duelo_actual_transformado = _transformar_id(mostrar_duelo)
        
        return duelo_actual_transformado
    else:
        duelo = {
            "usuario_uno_id": current_user["_id"],
            "usuario_dos_id": None,            
            "numero_de_ronda": 0,           
            "rondas_usuario_uno": [],    
            "rondas_usuario_dos": [],    
            "puntos_finales_usuario_uno": None,
            "puntos_finales_usuario_dos": None,
            "fecha_inicio": datetime.now(timezone.utc),
            "fecha_fin": None,                 
            "ganador_id": None                    
        }
        
        id = db_client.Duelos.insert_one(duelo).inserted_id
        nuevo_duelo = db_client.Duelos.find_one({"_id": id})
        duelo_transformado = _transformar_id(nuevo_duelo)
        return duelo_transformado



#un ronda duelo que tenga 3 preguntas por ronda.
    
    
    
def _transformar_id(doc: Dict) -> Dict:
    """Funcion encargada de formatear el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        doc["usuario_uno_id"] = str(doc["usuario_uno_id"])
        if doc["usuario_dos_id"]:
            doc["usuario_dos_id"] = str(doc["usuario_dos_id"])
    return doc

