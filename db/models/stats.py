from pydantic import BaseModel

class EstadisticasUsuario(BaseModel):
    id_usuario           : str
    duelos_jugados       : int = 0
    duelos_ganados       : int = 0
    duelos_perdidos      : int = 0
    preguntas_respondidas: int = 0
    preguntas_correctas  : int = 0
    preguntas_incorrectas: int = 0