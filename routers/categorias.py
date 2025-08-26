from fastapi import APIRouter
from db.models.categorias import Categoria
from service import service_categorias
from db.models.categorias import Categoria
from fastapi import HTTPException, status, Body

router = APIRouter(prefix="/Categoria",
                   tags=["CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Categorias"

@router.post("/Realizar/Carga", response_model=list[Categoria], status_code=status.HTTP_201_CREATED)
async def crear_categorias_endpoint(categorias: list[Categoria] = Body(...)):
    """
    Crea una o varias categorías en la base de datos.
    """
    nuevas_categorias = service_categorias.insertar_categorias(categorias)
    return nuevas_categorias