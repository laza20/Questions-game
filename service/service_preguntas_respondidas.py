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

def view_categories_principals(current_user) -> list[dict]:
    """
    Funcion encargada de retornar las estadisticas de las categorias principales
    """
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
        
        dict_porcentajes = _formar_dict_porcentajes(nombre_categoria, total, correcta, incorrecta, porcentaje_final)
        
        lista_porcentajes.append(dict_porcentajes)
        
    return lista_porcentajes                
                
def ver_porcentajes_categoria_particular(current_user, categoria):
    categoria_necesaria = db_client.Categorias.find_one({"nombre":{"$regex": f"^{categoria}$", "$options": "i"}})
    if not categoria_necesaria:
        _sin_categorias()
        
    id_categoria = categoria_necesaria["_id"]
    nombre_categoria = categoria_necesaria["nombre"]
    preguntas = list(db_client.Preguntas_respondidas.find({"id_usuario": current_user["_id"]}))
    if not preguntas:
        _sin_preguntas()

    categorias_descendentes = db_helpers.identificar_categorias_descentes_con_graphlookup(id_categoria)
    ids_descendentes = {doc for doc in categorias_descendentes}
    lista_preguntas = []
    for pregunta in preguntas:
        id_pregunta = pregunta["id_pregunta"]
        pregunta_guardada = db_client.Preguntas.find_one({"_id": id_pregunta})
        
        if not pregunta_guardada:
            continue 
            
        name_or_id_categoria = pregunta_guardada.get("categoria_id")
        
        id_categoria_asociada = db_helpers.get_categoria_id(name_or_id_categoria)
        oid_categoria_asociada = funciones_logicas.validate_object_id(id_categoria_asociada)
        
        if oid_categoria_asociada not in ids_descendentes:
            continue
        

        pregunta_por_categoria = {
            "pregunta": pregunta,
            "nombre": nombre_categoria
        }
        print(pregunta_por_categoria)
        
        lista_preguntas.append(pregunta_por_categoria)
    
    dict_porcentajes  = {}
    correcta = 0
    incorrecta = 0
    total = 0
    porcentaje_final=0
    for pregunta  in lista_preguntas:
        
        if pregunta["pregunta"]["respuesta"] == "CORRECTA":
            correcta += 1
        else:
            incorrecta += 1    
        
        total = correcta + incorrecta
        if total == 0:
            porcentaje_final = 0
        else:
            porcentajes = correcta / total
            porcentaje_final = round(porcentajes*100,2)
        
    dict_porcentajes = _formar_dict_porcentajes(nombre_categoria, total, correcta, incorrecta, porcentaje_final)
        
        
    return dict_porcentajes  
        
        
def _formar_dict_porcentajes(nombre_categoria, total, correcta, incorrecta, porcentaje_final):
    dict_porcentajes={"categoria":nombre_categoria,
                    "cantidad_de_preguntas":total,
                    "preguntas_acertadas":correcta,
                    "preguntas_erradas": incorrecta,
                    "porcentajes": porcentaje_final}
    
    return dict_porcentajes
    
    
def _sin_categorias():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontraron las categorias necesarias"
        )    

def _sin_preguntas():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontraron las preguntas necesarias"
        )