from fastapi import APIRouter
from db.models.questions import Question
from db.schemas.questions import question_schema, many_question_schema, many_request_schema
from service import service_questions



router = APIRouter(prefix="/Preguntas",
                   tags=["PREGUNTAS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Preguntas"

