from fastapi import APIRouter
from db.models.logros import LogrosGenerales, LogrosUsuario, LogrosNames
from service import service_logros
from fastapi import HTTPException, status, Body
from fastapi import APIRouter, Depends
from dependencias import get_current_user, is_primer_rango, is_segundo_rango, is_tercer_rango

router = APIRouter(prefix="/Logros",
                   tags=["LOGROS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Categorias"

@router.post("/Realizar/Carga", response_model=list[LogrosGenerales], status_code=status.HTTP_201_CREATED)
async def crear_categorias_endpoint(logros: list[LogrosGenerales] = Body(...), current_user: dict = Depends(is_tercer_rango)):
    """
    End point encargado de crear uno o varios logros en la base de datos.
    """
    nuevos_logros = service_logros.insertar_logros(logros, current_user)
    return nuevos_logros

@router.get("/Ver/Todo", response_model=list[LogrosGenerales], status_code=status.HTTP_202_ACCEPTED)
async def  view_old(current_user: dict = Depends(get_current_user)):
    """
    End point para mostrar una lista con todos los logros.
    """
    logros_totales = service_logros.ver_todos_los_logros()
    return logros_totales


@router.get("/Ver/Nombres", response_model=list[LogrosNames], status_code=status.HTTP_202_ACCEPTED)
async def view_achievement_names(current_user: dict = Depends(get_current_user)):
    """
    End point para ver todos los logros, solamente sus nombres
    """
    nombres_logros = service_logros.ver_todos_los_logros()
    return nombres_logros

#ver por todo por nombre, ver logro particular -> por nombre, ver por condicion (tipo).