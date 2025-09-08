from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Dict, List
from db.models.usuarios import Usuario
from datetime import datetime, timedelta, timezone
from utils import db_helpers
import secrets
from db.client import db_client

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 10
hex_token = secrets.token_hex(16) 
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
    
    return {"access_token": jwt.encode(acces_token,hex_token,algorithm=ALGORITHM), "token_type": "bearer"}



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