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
    End point encargado de crear una o varias categorías en la base de datos.
    """
    nuevas_categorias = service_categorias.insertar_categorias(categorias)
    return nuevas_categorias


@router.get("/Ver/Todo", response_model=list[Categoria], status_code=status.HTTP_202_ACCEPTED)
async def view_old_categories():
    """
    End point encargado de mostrar todos los documentos de categorias
    """
    categorias = service_categorias.visionar_todas_las_categorias()
    return categorias

@router.get("/Ver/Nivel/{grado}", response_model=list[Categoria], status_code=status.HTTP_202_ACCEPTED)
async def view_data_by_grade(grado: str):
    """
    End point que permite visionar una categoria por su grado.
    """
    categorias = service_categorias.visionar_categorias_por_nivel(grado)
    return categorias
    
@router.get("/Ver/Por/Categoria/{padre_id}", response_model=list[Categoria], status_code=status.HTTP_202_ACCEPTED)
async def view_data_by_padre_id(padre_id: str):
    """
    End point que permite visionar una categoria por su grado.
    """
    categorias = service_categorias.visionar_categorias_por_padre(padre_id)
    return categorias

@router.put("/Actaulizar/Id", response_model=list[Categoria], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_id():
    """
    End point que permite actualizar el id de str a Object id
    """
    service_categorias.modificar_id()