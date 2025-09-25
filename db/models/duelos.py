from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

class PreguntasUnitaria(BaseModel):
    pregunta_id       : str
    respuesta_correcta: bool
    puntos_pregunta   : int
    nivel_pregunta    : str
    
class PreguntasRonda(BaseModel):
    pregunta : List[PreguntasUnitaria] = Field(default_factory=list)

# Representa una sola ronda dentro de un duelo
class RondaDuelo(BaseModel):
    preguntas_ronda    : list[PreguntasRonda]
    puntos_obtenidos   : int
    tiempo_respuesta_ms: int

# El modelo de la colección 'duelos'
class Duelo(BaseModel):
    id                          : Optional[str] = None
    usuario_uno_id              : str
    usuario_dos_id              : Optional[str] = None
    numero_de_ronda             : Optional[int] = 0
    rondas_usuario_uno          : List[RondaDuelo] = Field(default_factory=list)
    rondas_usuario_dos          : List[RondaDuelo] = Field(default_factory=list)
    puntos_finales_usuario_uno  : Optional[int] = None
    puntos_finales_usuario_dos  : Optional[int] = None
    fecha_inicio                : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    fecha_fin                   : Optional[datetime] = None
    ganador_id                  : Optional[str] = None