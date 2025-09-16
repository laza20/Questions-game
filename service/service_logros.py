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

"""Inicio de llamadas al usuario """
def insertar_logros(logros: List[LogrosGenerales], current_user:dict) -> List[Dict]:
    """
    Función principal para validar e insertar uno o varios logros.
    """
    if not isinstance(logros, list) or not logros:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se espera una lista de logros.")
        
    documentos_a_insertar = []
    

    nombres_cargados = set()
    descripcion_cargadas = set()
    for logro in logros:
        
        key_nombre, key_condicion = _create_key(logro)
        if key_nombre in nombres_cargados or key_condicion in descripcion_cargadas:
            errores_simples.error_carga_repetida_un_solo_dato(f"{logro.nombre}-{logro.condicion}", "Logros")
        nombres_cargados.add(key_nombre)
        descripcion_cargadas.add(key_condicion)
        _validaciones_logros(logro)


        documento = logro.model_dump(by_alias=True, exclude_none=True)
        if logro.id:
            del documento["id"]
        documento["tipo"] = "Logro"
        documento["creador_id"] = current_user["_id"]
        documentos_a_insertar.append(documento)
        
    # Inserción en la base de datos
    coleccion = db_client.Logros
    if len(documentos_a_insertar) == 1:
        id = coleccion.insert_one(documentos_a_insertar[0]).inserted_id
        nuevos_documentos = [coleccion.find_one({"_id": id})]
    else:
        resultado = coleccion.insert_many(documentos_a_insertar)
        nuevos_documentos = list(coleccion.find({"_id": {"$in": resultado.inserted_ids}}))
        
    documentos = [_transformar_id(doc) for doc in nuevos_documentos]
            
    return documentos


def _validaciones_logros(logro):
    regex = re.compile(re.escape(logro.descripcion), re.IGNORECASE)
    if db_client.Logros.find_one({ "descripcion": regex }):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"La descripcion '{logro.descripcion}' ya se encuetra en un logro de la base de datos.")
    
    validaciones_simples.validacion_simple_general("Logros", logro.nombre)
        

def _create_key(dato: LogrosGenerales):
    """
    Funcion encargada de generar una key la cual permite verificar que los documentos
    ingresados no se repitan.
    """
    return dato.nombre.lower(), dato.descripcion.lower()

def _transformar_id(doc: Dict) -> Dict:
    """Funcion encargada de formatear el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
        if "creador_id" in doc and doc["creador_id"] is not None:
            doc["creador_id"] = str(doc["creador_id"])
    return doc

def _sin_logro():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontraron los logros necesarios"
        )