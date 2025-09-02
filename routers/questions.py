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

@router.get("/Ver/Todo", response_model=list[Question], status_code=status.HTTP_202_ACCEPTED)
async def view_old_categories():
    """
    End point encargado de mostrar todos los documentos de preguntas
    """
    preguntas = service_questions.visionar_todas_las_preguntas()
    return preguntas

@router.put("/Actualizar/Id", response_model=list[Question], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_id():
    """
    End point que permite actualizar el id de str a Object id
    """
    service_questions.modificar_id()

@router.get("/Random/General", response_model=QuestionRequest, status_code=status.HTTP_202_ACCEPTED)
async def view_question_random():
    """
    End point que llama a una pregunta aleatoria en general.
    """
    question = service_questions.play_question_random()
    return question

@router.get("/Categoria/Principal/{categoria}", response_model=QuestionRequest, status_code=status.HTTP_202_ACCEPTED)
async def view_question_by_category(categoria:str):
    """
    End point el cual retorna una pregunta de una categoria determinada.
    Funciona con todas las categorias de cualquier grado.
    """
    question = service_questions.play_question_by_category(categoria)
    return question


@router.get("/Duelo/General", response_model=list[QuestionRequest], status_code=status.HTTP_202_ACCEPTED)
async def view_many_questions_for_duel():
    """
    End point el cual retorna 10 preguntas para el duelo.
    """
    question = service_questions.play_duel()
    return question