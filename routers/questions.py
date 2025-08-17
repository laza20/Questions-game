from fastapi import APIRouter
from db.models.questions import Question
from db.schemas.nano_categorias import nano_categoria_schema,nano_categorias_schema
from peticiones_http import (
    peticiones_http_post,
    peticiones_http_get
)
from validaciones import validar_questions



router = APIRouter(prefix="/Preguntas",
                   tags=["PREGUNTAS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Preguntas"

peticiones_http_post.realizar_carga_unitaria(
    Question,
    router,
    base_de_datos,
    validar_questions.validacion_carga_question
)

peticiones_http_post.realizar_carga_masiva(
    Question,
    router,
    base_de_datos,
    validar_questions.validacion_carga_question
)