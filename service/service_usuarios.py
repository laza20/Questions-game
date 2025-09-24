from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
from typing import Dict, List
from db.models.usuarios import Usuario
from datetime import datetime, timedelta, timezone
from utils import db_helpers, funciones_logicas
from db.client import db_client

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 10
oauth2 = OAuth2PasswordBearer(tokenUrl="token")
crypt = CryptContext(schemes=["bcrypt"]  )

def insert_users(user: Usuario) -> List[Dict]:
    """
    Función principal para validar e insertar un usuario.
    """

    _validacion_usuario(user)
    documento = user.model_dump(by_alias=True, exclude_none=True)
    documento.pop("id", None)
    documento["password_hash"] = crypt.hash(user.password_hash)
    coleccion = db_client.Usuarios
    id = coleccion.insert_one(documento).inserted_id
    nuevo_documento = [coleccion.find_one({"_id": id})]
    resultado = _format_document(documento)
            
    return resultado

def login_user(usuario:OAuth2PasswordRequestForm = Depends())-> str:
    """
    Funcion la cual sirve para logear un usuario y darle un token
    """
    usuario_db = db_client.Usuarios.find_one({"nombre_usuario":usuario.username})
    if not usuario_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuario no encontrado")
    dict_usuario = dict(usuario_db)
    if not crypt.verify(usuario.password, dict_usuario["password_hash"]):
        raise HTTPException(
            status_code= 400, detail= "La contraseña es incorrecta")
        
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    acces_token = {"sub":dict_usuario["nombre_usuario"], "exp":expire}
    
    if dict_usuario.get("estado", False):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario esta inactivo")
    
    return {"access_token": jwt.encode(acces_token,SECRET_KEY,algorithm=ALGORITHM), "token_type": "bearer"}

def eliminar_logro(id_logro: str, current_user: dict) -> Dict:
    """
    Funcion encargada de eliminar un logro de un usuario.
    """
    oid_logro_a_eliminar = funciones_logicas.validate_object_id(id_logro)
    if not oid_logro_a_eliminar:
        _sin_logro()
    resultado_actualizacion = db_client.Usuarios.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"logros": oid_logro_a_eliminar}}
    )
    
    if resultado_actualizacion.modified_count == 1:
        usuario_actualizado = db_client.Usuarios.find_one({"_id": current_user["_id"]})
        
        # This is the crucial step: convert ObjectIds to strings before returning
        if usuario_actualizado and "logros" in usuario_actualizado:
            usuario_actualizado["logros"] = [str(logro_id) for logro_id in usuario_actualizado["logros"]]
            
        return usuario_actualizado
    else:
        # Also, make sure to handle the case where the user object is returned without an update
        if "logros" in current_user:
            current_user["logros"] = [str(logro_id) for logro_id in current_user["logros"]]
        return current_user

def _validacion_usuario(user:Usuario):
    
    if db_client.Usuarios.find_one({"mail_usuario":user.mail_usuario}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El mail ingresado ya esta asociado a una cuenta")
    
    if db_client.Usuarios.find_one ({"nombre_usuario":user.nombre_usuario}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= "El nombre de usuario ya existe en la base de datos")
    
def _format_document(doc: Dict) -> Dict:
    """Funcion que formatea el id para entregar un str en lugar de un object id."""
    if doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

def _sin_logro():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=f"No se encontrar al usuario necesario."
        )