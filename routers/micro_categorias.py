from fastapi import APIRouter
from db.models.micro_categorias import MicroCategoria
from db.schemas.micro_categorias import micro_categoria_schema,micro_categorias_schema
from peticiones_http import (
    peticiones_http_post
)
from validaciones import validar_micro_categoria



router = APIRouter(prefix="/Micro/Categoria",
                   tags=["MICRO CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Micro_categoria"

peticiones_http_post.cargar_uno(
    MicroCategoria,
    router,
    base_de_datos,
    micro_categoria_schema,
    validar_micro_categoria.validacion_carga_micro_categoria
)

peticiones_http_post.cargar_muchos(
    MicroCategoria,
    router,
    base_de_datos,
    micro_categorias_schema,
    validar_micro_categoria.validacion_carga_micro_categoria
)