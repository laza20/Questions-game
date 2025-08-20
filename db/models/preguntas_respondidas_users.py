from typing import Optional
from pydantic import BaseModel


class PreguntasRespondidas(BaseModel):
    id             : Optional[str] = None
    id_usuario     : Optional[str] = None
    id_pregunta    : Optional[str] = None
    cat_preg       : Optional[str] = None
    sub_cat_preg   : Optional[str] = None
    micro_cat_preg : Optional[str] = None
    nano_cat_preg  : Optional[str] = None
    