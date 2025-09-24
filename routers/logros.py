from fastapi import APIRouter
from db.models.logros import LogrosGenerales, LogrosUsuario, LogrosNames, LogrosGeneralesSinIds
from db.models.usuario_player import LogrosMostrar
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

@router.get("/view/old", response_model=list[LogrosGenerales], status_code=status.HTTP_202_ACCEPTED)
async def  view_old(current_user: dict = Depends(is_primer_rango)):
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

@router.get("/Ver/Todo", response_model=list[LogrosGeneralesSinIds], status_code=status.HTTP_202_ACCEPTED)
async def view_achievement_names(current_user: dict = Depends(get_current_user)):
    """
    End point para ver todos los logros sin ids(para usuarios generales).
    """
    logros_totales = service_logros.ver_todos_los_logros_sin_id()
    return logros_totales

@router.get("/Ver/Por/Tipo/{tipo}", response_model=list[LogrosGeneralesSinIds], status_code=status.HTTP_202_ACCEPTED)
async def view_achievement_types(tipo:str, current_user: dict = Depends(get_current_user)):
    """
    End point para ver todos los logros por tipo de logro.
    """
    logros_totales = service_logros.ver_logros_por_tipos(tipo)
    return logros_totales

@router.delete("/Eliminar/Logro/{id}}", response_model=list[LogrosGeneralesSinIds], status_code=status.HTTP_202_ACCEPTED)
async def delete_achievement_by_id(id:str, current_user: dict = Depends(is_primer_rango)):
    """
    End point encargado de eliminar un logro por medio de su id
    """
    
@router.get("/Ver/Logros/Simples/Usuario", response_model=LogrosMostrar, status_code=status.HTTP_202_ACCEPTED)
async def view_achievement_user_names(current_user: dict = Depends(get_current_user)):
    """
    End point encargado de visualizar los logros de un usuario (solo nombres).
    """
    logros = service_logros.view_logros_user_names(current_user)
    return logros


@router.get("/Ver/Logros/Totales/Usuario", response_model=list[LogrosGenerales], status_code=status.HTTP_202_ACCEPTED)
async def view_achievement_user_names( current_user: dict = Depends(get_current_user)):
    """
    End point encargado de visualizar los logros de un usuario.
    """
    logros = service_logros.view_logros_user(current_user)
    return logros