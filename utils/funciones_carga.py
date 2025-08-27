from db.client import db_client
from typing import List, Dict
from pymongo.results import InsertOneResult, InsertManyResult

def insertar_uno(documento: Dict, coleccion_nombre: str) -> Dict:
    """Inserta un único documento y retorna el documento insertado."""
    coleccion = getattr(db_client, coleccion_nombre)
    resultado: InsertOneResult = coleccion.insert_one(documento)
    nuevo_documento = coleccion.find_one({"_id": resultado.inserted_id})
    if nuevo_documento:
        nuevo_documento['id'] = str(nuevo_documento.pop('_id'))
    return nuevo_documento

def insertar_muchos(documentos: List[Dict], coleccion_nombre: str, base_de_datos: str) -> List[Dict]:
    """Inserta varios documentos y retorna los documentos insertados."""
    coleccion = getattr(db_client, coleccion_nombre)
    resultado: InsertManyResult = coleccion.insert_many(documentos)
    documentos_insertados = list(coleccion.find({"_id": {"$in": resultado.inserted_ids}}))
    for doc in documentos_insertados:
        doc['id'] = str(doc.pop('_id'))
    return documentos_insertados


