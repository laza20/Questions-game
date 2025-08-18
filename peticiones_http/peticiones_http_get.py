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
        
        
def jugar_categorias_generales(router, base_de_datos, schema, Clase: Type[BaseModel]):
    @router.get("/Jugar/Categoria/General", response_model=Clase)
    async def plays_game():
        question = funciones_randoms.jugar_preguntas_generales(base_de_datos, schema)
        return question