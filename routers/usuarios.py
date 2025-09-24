from fastapi import APIRouter,HTTPException, status, Depends
from db.models.usuarios import Usuario, UsarioLogeado, UsuarioCreado
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import service_usuarios
from dependencias import get_current_user, is_primer_rango, is_segundo_rango, is_tercer_rango

router = APIRouter(prefix="/Usuarios",
                   tags=["Usuarios"],
                   responses={404:{"Message":"No encontrado"}}
)


@router.post("/Registrarse", response_model=UsuarioCreado, status_code=status.HTTP_202_ACCEPTED)
async def create_user(user:Usuario):
    """
    End point encargado de crear un usuario.
    """
    usuario = service_usuarios.insert_users(user)
    return usuario


@router.post("/Login", status_code=status.HTTP_202_ACCEPTED)
async def logearse(usuario:OAuth2PasswordRequestForm = Depends()):
    """
    End point que sirve para loguearse el usuario.
    """
    logeado = service_usuarios.login_user(usuario)
    return logeado

@router.patch("/Eliminar/Logro/{id}", response_model=Usuario, status_code=status.HTTP_202_ACCEPTED)
async def delete_achievement_by_id_for_user(id:str, current_user: dict = Depends(is_primer_rango)):
    """
    End point encargado de eliminar un logro por medio de su id
    """
    usuario = service_usuarios.eliminar_logro(id, current_user)
    return usuario