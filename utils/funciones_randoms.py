import random
from db.client import db_client
from fastapi import HTTPException, status
from utils import db_helpers
from typing import Dict, List


def jugar_preguntas_generales():
    intentos_maximos = 10
    intentos = 0

    while intentos < intentos_maximos:
        # 1. Elegir un nivel y categoría de forma aleatoria.
        nivel_elegido = aleatorizar_niveles()
        categoria_elegida = aleatorizar_categorias_generales()
        
        documentos = db_helpers.seleccionar_pregunta(categoria_elegida, nivel_elegido)
        
        # Si se encuentra un documento, se sale del bucle y se retorna.
        if documentos:
            pregunta_elegida = documentos[0]
            pregunta_elegida["categoria_id"] = categoria_elegida
            return _format_document(pregunta_elegida)
        
        intentos += 1

def jugar_preguntas_de_una_categoria(base_de_datos, categoria):
    documentos = []
    while not documentos:
        nivel_elegido = aleatorizar_preguntas_de_una_categoria()
        coleccion = getattr(db_client, base_de_datos)
        documentos = list(coleccion.find({"nivel":{"$regex": f"^{nivel_elegido}$", "$options": "i"}, 
                        "categoria_id": {"$regex": f"^{categoria}$", "$options": "i"}}))
            
    pregunta_elegida = random.choice(documentos)
    return pregunta_elegida

#Sirve para cuando se quiere jugar a una categoria sola.
def aleatorizar_preguntas_de_una_categoria():
    nivel_elegido = aleatorizar_niveles()
    return nivel_elegido


#Sirve para cuando se quiere jugar en todas las categorias.
def aleatorizar_preguntas_generales():
    categoria_elegida = aleatorizar_categorias_generales()
    nivel_elegido     = aleatorizar_niveles()
    
    return nivel_elegido, categoria_elegida


def aleatorizar_niveles():
    niveles = ['facil', 'medio', 'dificil', 'imposible']
    probabilidades = [0.40, 0.30, 0.20, 0.10]
    
    nivel_elegido = random.choices(niveles, weights=probabilidades, k=1)
    return nivel_elegido[0]

def aleatorizar_categorias_generales():
    categorias = ["deportes","Entretenimiento","ciencia", "historia", "cultura general"]
    
    categoria_elegida = random.choices(categorias)
    
    return categoria_elegida[0]

def _format_document(doc: Dict) -> Dict:
    """Funcion que formatea el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        doc["categoria_id"] = str(doc["categoria_id"])
    return doc