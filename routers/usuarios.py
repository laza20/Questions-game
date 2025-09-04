from fastapi import APIRouter,HTTPException, status
from db.models.usuarios import Usuario, UsarioLogeado, UsuarioCreado
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


