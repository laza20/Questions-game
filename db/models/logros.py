from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

class LogrosGenerales(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: str
    puntos: int
    creador_id: Optional[str] = None  # Referencia al usuario que lo creó
    condicion: Dict[str, Any] # Ej: {"tipo": "duelos_ganados", "valor": 100}
    
class LogrosUsuario(BaseModel):
    id_logro   : str
    id_usuario : str
    fecha_obtenido: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
