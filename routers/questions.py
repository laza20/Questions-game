from fastapi import APIRouter
from db.models.questions import Question, QuestionRequest
from service import service_questions
from fastapi import status, Body
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder



router = APIRouter(prefix="/Preguntas",
                   tags=["PREGUNTAS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Preguntas"

@router.post("/Realizar/Carga", response_model=list[QuestionRequest], status_code=status.HTTP_201_CREATED)
async def crear_questions_endpoint(question: list[Question] = Body(...)):
    """
    Crea una o varias categorías en la base de datos.
    """
    nuevas_preguntas = service_questions.insertar_question(question)
    return nuevas_preguntas 


