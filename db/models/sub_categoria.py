from pydantic import BaseModel

class SubCategoria(BaseModel):
    id                  : str | None = None
    nombre              : str
    descripcion         : str
    categoria_principal : str
    tipo                : str | None = None
    estado              : bool