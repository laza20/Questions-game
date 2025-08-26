from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Question(BaseModel):
    id                 : Optional[str]      = None
    pregunta           : str
    opciones           : List[str]
    respuesta_correcta : str
    categoria_id       : str
    puntos_pregunta    : Optional[int]      = None
    nivel              : Optional[str]      = None
    consecutiva        : Optional[int]      = None
    usuario_carga      : Optional[str]      = None
    fecha_carga        : Optional[datetime] = None
    tipo               : Optional[str]      = None
    estado             : Optional[bool]     = None

class QuestionRequest(BaseModel):
    pregunta          : str
    opciones          : List[str]
    respuesta_correcta: str
    nivel             : str
    categoria         : str