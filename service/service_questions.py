from fastapi import HTTPException, status
from db.client import db_client
from validaciones_generales import validaciones_simples, validaciones_dobles
from errores_generales import errores_simples
from funciones import funcion_carga_questions
import re



def validacion_carga_question(datos, base_de_datos):
    coleccion = (db_client, base_de_datos)
    if isinstance(datos, list) and len(datos) >= 2:
        questions = set()
        for dato in datos:
            key = validacion_carga_question_2(dato, base_de_datos, coleccion)
            validar_carga_repetida(key, questions, dato, base_de_datos)
            questions.add(key)   
    else:
        dato = datos if not isinstance(datos, list) else datos[0]
        key = validacion_carga_question_2(dato, base_de_datos, coleccion)
            
def validar_carga_repetida(key, questions, dato, base_de_datos):
    if key in questions:
       errores_simples.error_carga_repetida_un_solo_dato(dato.pregunta, base_de_datos)
            
def validacion_carga_question_2(dato, base_de_datos, coleccion):
    key = create_key(dato)
    pattern = f"^{re.escape(dato.pregunta.strip())}$"
    if db_client.Preguntas.find_one({"pregunta": {"$regex": pattern, "$options": "i"}}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"Pregunta ya existente: {dato.pregunta}"
        )
    validar_cantidad_de_opciones(dato)
    return key

def validar_cantidad_de_opciones(dato):
    opciones = 0
    for opcion in dato.opciones:
        opciones += 1 
    if opciones > 4:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No puede ingresar mas de 4 opciones")

def create_key(dato):
    key = (dato.pregunta.lower())   
    return key



    