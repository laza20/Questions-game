from fastapi import APIRouter
from db.models.duelos import Duelo,PreguntasRonda,RondaDuelo
from service import service_duelos
from fastapi import HTTPException, status, Body
from fastapi import APIRouter, Depends
from dependencias import get_current_user, is_primer_rango, is_segundo_rango, is_tercer_rango

router = APIRouter(prefix="/Duelos",
                   tags=["DUELOS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Duelos"


@router.post("/Crear", response_model=Duelo, status_code=status.HTTP_201_CREATED)
async def crear_duelos(current_user: dict = Depends(get_current_user)):
    """
    End point que cumple la funcion de iniciar un duelo.
    """
    duelo = service_duelos.iniciar_duelo(current_user)
    return duelo