from fastapi import APIRouter
from db.models.nano_categoria import NanoCategoria
from db.schemas.nano_categorias import nano_categoria_schema,nano_categorias_schema
from peticiones_http import (
    peticiones_http_post,
    peticiones_http_get
)
from validaciones import validar_nano_categoria



router = APIRouter(prefix="/Nano/Categoria",
                   tags=["NANO CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Nano_categoria"

peticiones_http_post.cargar_uno(
    NanoCategoria,
    router,
    base_de_datos,
    nano_categoria_schema,
    validar_nano_categoria.validacion_carga_nano_categoria
)

peticiones_http_post.cargar_muchos(
    NanoCategoria,
    router,
    base_de_datos,
    nano_categorias_schema,
    validar_nano_categoria.validacion_carga_nano_categoria
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    NanoCategoria, 
    nano_categorias_schema)