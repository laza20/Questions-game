from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Category(BaseModel):
    categoria:  Optional[str] = None
    sub_categoria: Optional[str] = None
    micro_categoria: Optional[str] = None
    nano_categoria: Optional[str] = None

class Question(BaseModel):
    id: str | None = None
    pregunta: str
    opciones: List[str]
    respuesta_correcta: str
    categoria: Category  # Aquí la jerarquía es un modelo anidado
    puntos_pregunta : Optional[int] = None
    nivel  : Optional[str] = None
    usuario_carga: str
    fecha_carga: Optional[datetime] = None
    tipo: Optional[str] = None
    estado: bool

class QuestionRequest(BaseModel):
    pregunta          : str
    opciones          : List[str]
    respuesta_correcta: str
    nivel             : str
    categoria         : Dict[str, Optional[str]]