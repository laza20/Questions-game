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


def orquestador_logros(current_user, evento, datos_evento):
    """
    Funcion orquestadora, recibe, el usuario que esta jugando, 
    el evento (pregunta respondida, duelo ganado) 
    y datos del evento (categoria, respuesta)
    """
    
    if evento == "pregunta_respondida":
        es_correcta = datos_evento.get("es_correcta", False)
        categoria = datos_evento.get("categoria")
        dificultad = datos_evento.get("dificultad")

        if es_correcta:
            db_client.Usuarios.update_one(
                {"_id": current_user["_id"]},
                {"$inc": {"progreso.preguntas_correctas": 1}}
            )
            
            if categoria:
                campo_categoria = f"progreso.preguntas_{categoria}_correctas"
                db_client.Usuarios.update_one(
                    {"_id": current_user["_id"]},
                    {"$inc": {campo_categoria: 1}}
                )
            if dificultad:
                campo_dificultad = f"progreso.preguntas_{dificultad}_correctas"
                db_client.Usuarios.update_one(
                    {"_id": current_user["_id"]},
                    {"$inc": {campo_dificultad: 1}}
                )
        
        usuario_actualizado = db_client.Usuarios.find_one({"_id": current_user["_id"]})
        
        # Trigger all relevant verifiers
        verificador_preguntas_correctas(usuario_actualizado)

def verificador_preguntas_correctas(current_user):
    logros = list(db_client.Logros.find({"condicion.tipo": "preguntas_correctas"}))
    contador = current_user["progreso"]["preguntas_correctas"]

    for logro in logros:
        if str(logro["_id"]) not in [str(l) for l in current_user.get("logros", [])]:
            if logro["condicion"]["valor"] <= contador:
                current_user["logros"].append(logro["_id"])

    db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$set": {"logros": current_user["logros"]}}
    )

    return current_user
                
 