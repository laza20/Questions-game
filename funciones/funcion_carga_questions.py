from bson import ObjectId
from fastapi import HTTPException, status
from typing import List, Optional, Union
from db.client import db_client
from db.models.questions import QuestionRequest
from db.models.questions import Question as QuestionDB
from db.schemas.questions import question_schema, schema_request
from datetime import datetime
from validaciones import validar_questions

# --- Funciones de Lógica de Negocio ---
def validar_y_obtener_jerarquia_de_categoria(categoria_data: dict):
    """
    Valida la jerarquía de la categoría en una sola consulta
    y retorna la jerarquía completa.
    """
    # 1. Obtenemos el nivel más específico que el usuario envió
    #si se carga la nano categoria si o si debe cargarse la micro.
    #si la micro categoria eta repetida en la base de datos se pedira que tambien carge la sub categoria.
    nano_categoria  = categoria_data.get("nano_categoria")
    micro_categoria = categoria_data.get("micro_categoria")
    sub_categoria   = categoria_data.get("sub_categoria")
    categoria       = categoria_data.get("categoria")
    

    if micro_categoria and not sub_categoria:
        count = db_client.Micro_categoria.count_documents({"nombre": micro_categoria})
        if count > 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"La micro_categoria '{micro_categoria}' es ambigua. Por favor, especifique la sub_categoria.")
    
    
    filtro = {}
    if nano_categoria and not micro_categoria:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Acaba de ingresar una nano categoria, debe ingresar su micro categoria de manera obligatoria.")
    
    if not db_client.Nano_categoria.find_one({"nombre":{"$regex": f"^{nano_categoria}$", "$options": "i"}}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La nano categoria que acaba de ingresar no existe en la base de datos.")
    
    
    if nano_categoria and micro_categoria and not sub_categoria:
        filtro.update(obtener_datos_por_micro_categoria(micro_categoria))
        filtro["nano_categoria"]  = nano_categoria
    elif nano_categoria and micro_categoria and sub_categoria:
        filtro.update(obtener_categoria(sub_categoria))
        filtro["micro_categoria"] = micro_categoria
        filtro["nano_categoria"]  = nano_categoria
    elif micro_categoria:
        filtro.update(obtener_datos_por_micro_categoria(micro_categoria))
    elif sub_categoria:
       filtro.update(obtener_categoria(sub_categoria))
    elif categoria:
        filtro["categoria"] = categoria
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Al menos debe ingresar una categoria principal para la pregunta")


    return {
        "categoria"      : filtro.get("categoria"),
        "sub_categoria"  : filtro.get("sub_categoria"),
        "micro_categoria": filtro.get("micro_categoria"),
        "nano_categoria" : filtro.get("nano_categoria")
    }

# --- Funciones de Carga de Documentos ---


def obtener_categoria(sub_categoria):
    sub_categoria_data = db_client.Sub_categoria.find_one({"nombre": {"$regex": f"^{sub_categoria}$", "$options": "i"}})
    
    if not sub_categoria_data:
        raise HTTPException(status_code=404, detail=f"Sub_categoria '{sub_categoria}' no encontrada")
    categoria = sub_categoria_data["categoria_principal"]
    return {
        "sub_categoria": sub_categoria,
        "categoria": categoria
    }
    

def obtener_datos_por_micro_categoria(micro_categoria):
    dict_micro_categoria = db_client.Micro_categoria.find_one({"nombre": {"$regex": f"^{micro_categoria}$", "$options": "i"}})
    if not dict_micro_categoria:
        raise HTTPException(status_code=404, detail=f"Micro_categoria '{micro_categoria}' no encontrada")

    sub_categoria_data = db_client.Sub_categoria.find_one({"nombre": dict_micro_categoria["sub_categoria"]})
    if not sub_categoria_data:
        raise HTTPException(status_code=404, detail=f"Sub_categoria '{dict_micro_categoria['sub_categoria']}' no encontrada")

    categoria_data = sub_categoria_data["categoria_principal"]
    return {
        "micro_categoria": micro_categoria,
        "sub_categoria": sub_categoria_data["nombre"],
        "categoria": categoria_data
    }



def cargar_documentos(datos, base_de_datos, validacion):
    """
    Función genérica para cargar uno o varios documentos.
    """
    coleccion = getattr(db_client, base_de_datos)
    es_lista = isinstance(datos, list)
    lista_documentos = datos if es_lista else [datos]
    
    documentos_a_insertar = []
    validacion(lista_documentos, base_de_datos)
    for dato in lista_documentos:
        
        dict_dato = dato.model_dump()
        
        # Validamos y obtenemos la jerarquía en una sola llamada
        dict_dato["categoria"] = validar_y_obtener_jerarquia_de_categoria(dict_dato["categoria"])
        # Agregamos los campos del sistema
        dict_dato.update({
            "usuario_carga": "usuario_autenticado", 
            "fecha_carga": datetime.now(),
            "tipo" : base_de_datos,
            "estado": True
        })
        del dict_dato["id"]
        documentos_a_insertar.append(dict_dato)
        
    
    # Insertamos en la base de datos de forma eficiente
    if es_lista:
        resultado = coleccion.insert_many(documentos_a_insertar)
        documentos_insertados = coleccion.find({"_id": {"$in": resultado.inserted_ids}})
        return [schema_request(doc) for doc in documentos_insertados]
    else:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        documentos_insertados = coleccion.find_one({"_id": id})
        return schema_request(documentos_insertados)