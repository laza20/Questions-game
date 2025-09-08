from fastapi import APIRouter,HTTPException, status, Depends
from db.models.usuarios import Usuario, UsarioLogeado, UsuarioCreado
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from service import service_usuarios

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

