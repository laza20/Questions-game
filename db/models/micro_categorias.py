from pydantic import BaseModel

class MicroCategoria(BaseModel):
    id                  : str | None = None
    nombre              : str
    descripcion         : str
    sub_categoria       : str
    tipo                : str | None = None
    estado              : bool