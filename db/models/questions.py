from datetime import datetime, timezone
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Question(BaseModel):
    id                 : Optional[str]      = None
    pregunta           : str
    opciones           : List[str]
    respuesta_correcta : str
    categoria_id       : str
    puntos_pregunta    : Optional[int]      = 500
    nivel              : Optional[str]      = "Medio"
    consecutiva        : Optional[int]      = 0
    usuario_carga      : Optional[str]      = "Master"
    fecha_carga        : Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    tipo               : Optional[str]      = "Preguntas"
    estado             : Optional[bool]     = True

class QuestionRequest(BaseModel):
    id                : str
    pregunta          : str
    opciones          : List[str]
    respuesta_correcta: str
    nivel             : str
    categoria_id      : str
    usuario_carga     : str
    
class Respuesta(BaseModel):
    id                 : str
    respuesta_correcta : str  
    respuesta_acertada : str
    
class QuestionAnswer(BaseModel):
    id             : str
    pregunta       : str
    opciones       : str
    nivel          : str
    categoria_id   : str
    usuario_carga  : str