from fastapi import APIRouter
from db.models.questions import Question
from db.schemas.questions import question_schema, many_question_schema, many_request_schema
from peticiones_http import (
    peticiones_http_post,
    peticiones_http_get, 
    peticiones_http_put
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

peticiones_http_get.view_old_data(
    router, 
    base_de_datos, 
    Question, 
    many_question_schema
)

peticiones_http_put.agregar_puntos(
    router, 
    base_de_datos, 
    many_question_schema)
