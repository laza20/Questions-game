from datetime import datetime, timezone
from pydantic import BaseModel, Field

class PreguntasRespondidas(BaseModel):
    id                    : str = Field(None, alias="_id")
    id_usuario            : str
    id_pregunta           : str
    respuesta_del_usuario : str
    respuesta             : str
    puntos_obtenidos      : int
    timestamp             : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class CategoriasPorcentajes(BaseModel):
    categoria             : str
    cantidad_de_preguntas : int
    preguntas_acertadas   : int
    preguntas_erradas     : int
    porcentajes           : float

    
