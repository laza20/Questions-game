from fastapi import APIRouter
from db.models.sub_categoria import SubCategoria
from db.schemas.sub_categoria import sub_categoria_schema,sub_categorias_schema
from peticiones_http import (
    peticiones_http_post,
    peticiones_http_get
)
from validaciones import validar_sub_categoria



router = APIRouter(prefix="/Sub/Categoria",
                   tags=["SUB CATEGORIA"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Sub_categoria"

peticiones_http_post.cargar_uno(
    SubCategoria,
    router,
    base_de_datos,
    sub_categoria_schema,
    validar_sub_categoria.validacion_carga_sub_categoria
)

peticiones_http_post.cargar_muchos(
    SubCategoria,
    router,
    base_de_datos,
    sub_categorias_schema,
    validar_sub_categoria.validacion_carga_sub_categoria
)

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    SubCategoria, 
    sub_categorias_schema
    )

lista_de_propiedades = ["nombre", "descripcion"] 
peticiones_http_get.view_one_document_for_data_str(
    router, 
    base_de_datos, 
    sub_categoria_schema, 
    lista_de_propiedades
    )

peticiones_http_get.view_names_sub_categories(
    router, 
    base_de_datos, 
    sub_categorias_schema
)