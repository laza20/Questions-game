from pydantic import BaseModel

class Categoria(BaseModel):
    id                       : str | None = None
    nombre_categoria         : str
    descripcion              : str
    tipo                     : str | None = None
    estado                   : bool
    