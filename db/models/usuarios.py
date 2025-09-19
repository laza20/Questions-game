from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# Subdocumentos incrustados
class Stats(BaseModel):
    nivel                : int = 1
    puntos_xp            : int = 0

class PreguntasCreadas(BaseModel):
    id_pregunta    : Optional[str] = None
    
class Favorito(BaseModel):
    id_categoria : Optional[str] = None

class Progreso(BaseModel):
    preguntas_correctas                :Optional[int] = 0
    preguntas_muy_faciles_correctas    :Optional[int] = 0
    preguntas_faciles_correctas        :Optional[int] = 0
    preguntas_medio_correctas          :Optional[int] = 0
    preguntas_dificil_correctas        :Optional[int] = 0
    preguntas_imposible_correctas      :Optional[int] = 0
    preguntas_infinito_correctas       :Optional[int] = 0
    preguntas_deportes_correctas       :Optional[int] = 0
    preguntas_ciencia_correctas        :Optional[int] = 0
    preguntas_cultura_general_correctas:Optional[int] = 0
    preguntas_entretenimiento_correctas:Optional[int] = 0
    preguntas_historia_correctas       :Optional[int] = 0
    duelos_ganados                     :Optional[int] = 0



class Control(BaseModel):
    ultimo_login        : Optional[datetime] = None
    fecha_creacion      : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion : Optional[datetime] = None
    tipo                : Optional[str] = "Player"
    estado              : Optional[bool] = True

# Documento principal de la colección 'usuarios'
class Usuario(BaseModel):
    id               : Optional[str] = None
    nombre_usuario   : str
    mail_usuario     : EmailStr
    password_hash    : str
    nombre           : str
    apellido         : str
    rango            : Optional[str] = "User" #Rangos = User, Editor, Moderador, Admin
    fecha_nacimiento : datetime
    avatar_url       : Optional[str] = None
    descripcion      : Optional[str] = None
    stats            : Stats = Field(default_factory=Stats)
    logros           : Optional[List[str]] = Field(default_factory=list)
    progreso         : Optional[Progreso] = Field(default_factory=Progreso)
    favoritos        : Optional[List[Favorito]] = Field(default_factory=list)
    preguntas        : Optional[List[PreguntasCreadas]] = Field(default_factory=list)
    control          : Control = Field(default_factory=Control)
    
class UsuarioCreado(BaseModel):
    nombre_usuario   : str
    mail_usuario     : EmailStr
    password_hash    : str
    fecha_nacimiento : datetime
    
class UsarioLogeado(BaseModel):
    nombre_usuario   : str
    mail_usuario     : EmailStr
    avatar_url       : Optional[str] = None
    
class UsuarioPlayer(BaseModel):
    nombre_usuario   : str
    stats            : Stats = Field(default_factory=Stats)
    


