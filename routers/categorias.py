from fastapi import APIRouter
from db.models.categorias import Categoria
from db.schemas.categorias import categoria_schema,categorias_schema
from peticiones_http import (
    peticiones_http_post,
    peticiones_http_get
)
from validaciones import validar_categorias



router = APIRouter(prefix="/Categoria",
                   tags=["CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Categoria"

peticiones_http_post.cargar_uno(
    Categoria,
    router,
    base_de_datos,
    categoria_schema,
    validar_categorias.validacion_carga_categoria
)

peticiones_http_post.cargar_muchos(
    Categoria,
    router,
    base_de_datos,
    categorias_schema,
    validar_categorias.validacion_carga_categoria
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Categoria, 
    categorias_schema)