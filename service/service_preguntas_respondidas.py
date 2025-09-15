from utils import funcion_nivel_pregunta
from datetime import datetime, timezone
import re
from typing import Dict, List
from fastapi import HTTPException, status
from db.models.questions import Question
from db.client import db_client
from utils import (
    db_helpers, 
    funciones_logicas, 
    funciones_randoms, 
    graphlookups, 
    funcion_nivel_pregunta,
    funcion_niveles_usuario,
    puntos_usuario_por_pregunta
    )
from exceptions import errores_simples
import random

def view_categories_principals(current_user):
    preguntas = list(db_client.Preguntas_respondidas.find({"id_usuario": current_user["_id"]}))
    if not preguntas:
        _sin_preguntas()

    lista_preguntas = []
    for pregunta in preguntas:
        id_pregunta = pregunta["id_pregunta"]
        pregunta_guardada = db_client.Preguntas.find_one({"_id":id_pregunta})
        if not pregunta_guardada:
            _sin_preguntas()
        name_or_id_categoria = pregunta_guardada["categoria_id"]
        id_categoria = db_helpers.get_categoria_id(name_or_id_categoria)
        # 'categoria_principal' is now the full document (a dictionary)
        categoria_principal = db_helpers.identificar_categoria_con_graphlookup(id_categoria)

        pregunta_por_categoria = {
            "pregunta": pregunta,
            "categoria_principal": categoria_principal.get("nombre") # Get the name from the document
        }
        
        lista_preguntas.append(pregunta_por_categoria)
        
    categorias_principales = ["Deportes", "Entretenimiento", "Historia", "Ciencia", "Cultura General"]
    dict_porcentajes  = {}
    lista_porcentajes = []
    
    for categoria_doc  in categorias_principales:
        correcta = 0
        incorrecta = 0
        nombre_categoria = categoria_doc
        if not nombre_categoria:
            continue # Skip if the name is not found
        for pregunta in lista_preguntas:
            categoria_actual = pregunta["categoria_principal"]
            if categoria_actual.capitalize() == nombre_categoria.capitalize(): # Use .capitalize() on the string
                if pregunta["pregunta"]["respuesta"] == "CORRECTA":
                    correcta += 1
                else:
                    incorrecta += 1    
        
        total = correcta + incorrecta
        if total != 0:
            porcentajes = correcta / total
            porcentaje_final = round(porcentajes*100,2)
        else:
            porcentaje_final = 0
        dict_porcentajes={"categoria":nombre_categoria,
                        "cantidad_de_preguntas":total,
                        "preguntas_acertadas":correcta,
                        "preguntas_erradas": incorrecta,
                        "porcentajes": porcentaje_final}
        
        lista_porcentajes.append(dict_porcentajes)
        
    return lista_porcentajes                
                
        
    
    
def _sin_preguntas():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontraron las preguntas necesarias"
        )