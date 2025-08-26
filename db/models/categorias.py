from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class Categoria(BaseModel):
    id              : Optional[str] = Field(alias="_id", default=None)
    nombre          : str
    grado           : str 
    descripcion     : Optional[str]  = None
    padre_id        : Optional[str]  = None  # References the parent category's ID
    creador_id      : Optional[str]  = "Master"
    fecha_carga     : datetime       = Field(default_factory=lambda: datetime.now(timezone.utc))
    estado          : Optional[bool] = True
    
#los grados solo los puede crear el grupo de desarrollo.
#en primera instancia solo existiran 
#primer  
#segundo
#tercer
#cuarto