from fastapi import APIRouter
from db.models.categorias import Categoria
from service import service_categorias
from db.models.categorias import Categoria



router = APIRouter(prefix="/Categoria",
                   tags=["CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Categoria"









peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Categoria
    )

lista_de_propiedades = ["nombre", "descripcion"] 
peticiones_http_get.view_one_document_for_data_str(
    router, 
    base_de_datos, 
    lista_de_propiedades
    )