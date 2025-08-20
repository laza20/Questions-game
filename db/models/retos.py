from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

# Un documento de la colección 'retos'
class Reto(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    creador_id: Optional[str] = None  # Referencia al usuario que lo creó
    nombre_reto: str
    puntos_reto: int # Puntos totales a ganar en el reto
    categoria_id: str # Referencia a la categoría principal del reto
    preguntas: List[str] # Lista de IDs de las preguntas del reto
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))