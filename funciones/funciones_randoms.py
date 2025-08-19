import random
from db.client import db_client
from fastapi import HTTPException, status


def jugar_preguntas_generales(base_de_datos):
    documentos = []
    while not documentos:
        nivel_elegido, categoria_elegida = aleatorizar_preguntas_generales()
        coleccion = getattr(db_client, base_de_datos)
        documentos = list(coleccion.find({"nivel":{"$regex": f"^{nivel_elegido}$", "$options": "i"}, 
                        "categoria.categoria": {"$regex": f"^{categoria_elegida}$", "$options": "i"}}))
            
    pregunta_elegida = random.choice(documentos)
    return pregunta_elegida

def jugar_preguntas_de_una_categoria(base_de_datos, categoria):
    documentos = []
    while not documentos:
        nivel_elegido = aleatorizar_preguntas_de_una_categoria()
        coleccion = getattr(db_client, base_de_datos)
        documentos = list(coleccion.find({"nivel":{"$regex": f"^{nivel_elegido}$", "$options": "i"}, 
                        "categoria.categoria": {"$regex": f"^{categoria}$", "$options": "i"}}))
            
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