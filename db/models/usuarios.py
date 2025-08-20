from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# Subdocumentos incrustados
class Stats(BaseModel):
    nivel                : int = 1
    puntos_xp            : int = 0

    
class PreguntasCreadas(BaseModel):
    id_pregunta    : Optional[str] = None
    cat_preg       : Optional[str] = None
    sub_cat_preg   : Optional[str] = None
    micro_cat_preg : Optional[str] = None
    nano_cat_preg  : Optional[str] = None
    

class Favorito(BaseModel):
    categoria_fav       : Optional[str] = None
    sub_categoria_fav   : Optional[str] = None
    micro_categoria_fav : Optional[str] = None
    nano_categoria_fav  : Optional[str] = None



class Control(BaseModel):
    ultimo_login        : Optional[datetime] = None
    fecha_creacion      : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_actualizacion : Optional[datetime] = None
    tipo                : Optional[str] = "Player"
    estado              : Optional[bool] = True

# Documento principal de la colección 'usuarios'
class Usuario(BaseModel):
    id               : Optional[str] = Field(alias="_id", default=None)
    nombre_usuario   : str
    mail_usuario     : EmailStr
    password_hash    : str
    nombre           : str
    apellido         : str
    fecha_nacimiento : datetime
    avatar_url       : Optional[str] = None
    descripcion      : Optional[str] = None
    stats            : Stats = Field(default_factory=Stats)
    logros           : List[str] = Field(default_factory=list)
    retos            : List[str] = Field(default_factory=list)
    favoritos        : List[Favorito] = Field(default_factory=list)
    preguntas        : List[PreguntasCreadas] = Field(default_factory=list)



