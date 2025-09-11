from pydantic import BaseModel, Field, EmailStr
from db.models.usuarios import UsuarioPlayer
from db.models.questions import Respuesta

class RespuestaUsuario (BaseModel):
    usuario   : UsuarioPlayer
    respuesta : Respuesta

