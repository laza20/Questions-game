from pydantic import BaseModel

class NanoCategoria(BaseModel):
    id                  : str | None = None
    nombre              : str
    descripcion         : str
    micro_categoria     : str
    tipo                : str | None = None
    estado              : bool