from pydantic import BaseModel, Field, EmailStr
from db.models.usuarios import UsuarioPlayer
from db.models.questions import Respuesta
from db.models.logros import LogrosNames


class RespuestaUsuario (BaseModel):
    usuario   : UsuarioPlayer
    respuesta : Respuesta
    
    
class LogrosMostrar(BaseModel):
    usuario : UsuarioPlayer
    logros  : list[LogrosNames]

