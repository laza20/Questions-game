from fastapi import APIRouter
from db.models.questions import Question, QuestionRequest,QuestionAnswer,Respuesta
from db.models.preguntas_respondidas_users import CategoriasPorcentajes
from service import service_preguntas_respondidas
from fastapi import status, Body
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from dependencias import get_current_user 

router = APIRouter(prefix="/Preguntas_Respondidas",
                   tags=["PREGUNTAS RESPONDIDAS POR USUARIO"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Preguntas_respondidas"

@router.get("/Porcentaje/Categorias",response_model=list[CategoriasPorcentajes], status_code=status.HTTP_202_ACCEPTED)
async def view_categories_characters( current_user: dict = Depends(get_current_user)):
    """
    End point con la finalidad de mostrar los porcentajes de respuestas de usuario en las diversas categorias principales
    """
    porcentajes = service_preguntas_respondidas.view_categories_principals(current_user)
    return porcentajes

