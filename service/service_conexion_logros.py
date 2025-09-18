# In services/service_logros.py
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.logros import LogrosGenerales
from db.client import db_client
from bson.objectid import ObjectId
from utils import db_helpers, funciones_logicas
from typing import Optional
from validaciones_generales import validaciones_simples
import re
from utils import db_helpers
from exceptions import errores_simples


def orquestador_logros(current_user):
    preguntas_respondidas = list(db_client.Preguntas_respondidas.find({"id_usuario":current_user["_id"]}))
    verificador_preguntas_correctas(preguntas_respondidas, current_user)

    
    
def verificador_preguntas_correctas(preguntas_respondidas, current_user):
    logros = list(db_client.Logros.find({"tipo":"Logro", "condicion.tipo":"preguntas_correctas"}))
    contador = 0
    for pregunta in preguntas_respondidas:
        if pregunta["respuesta"] == "CORRECTA":
            contador += 1
    
    lista_logros = []
    for logro in logros:
        if logro["condicion"]["valor"] <= contador:
            lista_logros.append(logro)
    
    for logro in lista_logros:
        if logro["_id"] in current_user["logros"]:
            continue
        else:
            current_user["logros"].append(logro["_id"])
        
        
    db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"logros": current_user["logros"]}}
    )
    
    return current_user
                
 