#pyright: reportInvalidTypeForm=false
from funciones import funciones_logicas
from fastapi import status
from pydantic import BaseModel
from db.client import db_client
from typing import Type, List
from funciones import funciones_logicas
from fastapi import  HTTPException, status
from bson import ObjectId
from funciones import funciones_randoms



def view_old_data(router, base_de_datos, Clase: Type[BaseModel], schema):
    @router.get("/Ver/Todo", response_model=list[Clase])
    async def show_many_data():
        coleccion = getattr(db_client, base_de_datos)
        return schema(coleccion.find())
    
def view_one_document_for_data_str(router, base_de_datos, schema, lista_de_propiedades):
    @router.get("/Dato/{data}")
    async def show_many_data_for_data(data:str):
        coleccion = getattr(db_client, base_de_datos)
        for propiedad in lista_de_propiedades:
            resultado = coleccion.find_one({propiedad:{"$regex": f"^{data}$", "$options": "i"}})
            if resultado:
                return schema(resultado)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro ningun documento con ese dato")  
        
def view_names_sub_categories(router, base_de_datos, schema):
    @router.get("/Categoria/{categoria_principal}")
    async def show_type_categori(categoria_principal:str):
        coleccion = getattr(db_client, base_de_datos)
        documentos = schema(coleccion.find({"tipo":base_de_datos, "categoria_principal":categoria_principal}))
        if not documentos:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"No se encontraron documentos para la base de datos {base_de_datos}")
        lista_nombres = []
        campo = "nombre"
        for documento in documentos:
            nombre_doct = documento[campo]
            lista_nombres.append(nombre_doct)
        
        return lista_nombres
    
        
        
def view_question_random(router, base_de_datos, schema, Clase: Type[BaseModel]):
    @router.get("/Ver/Pregunta/Random/General", response_model=Clase)
    async def view_question_random():
        question = funciones_randoms.jugar_preguntas_generales(base_de_datos)
        return question
    
    
def play_question_general_random(router, base_de_datos):
    @router.get("/Jugar/Pregunta/Random/General")
    async def play_question_random():
        dict_question = {}
        question = funciones_randoms.jugar_preguntas_generales(base_de_datos)
        dict_question = {
            "pregunta": question["pregunta"],
            "opciones":question["opciones"],
            "respuesta_correcta":question["respuesta_correcta"],
            "nivel":question["nivel"]
        }
        return dict_question