from fastapi import APIRouter
from db.models.questions import Question, QuestionRequest,QuestionAnswer,Respuesta
from db.models.usuario_player import RespuestaUsuario
from service import service_questions
from fastapi import status, Body
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends
from dependencias import get_current_user, is_segundo_rango, is_tercer_rango, is_primer_rango



router = APIRouter(prefix="/Preguntas",
                   tags=["PREGUNTAS"],
                   responses={404:{"Message":"No encontrado"}}
)
base_de_datos = "Preguntas"

@router.post("/Realizar/Carga", response_model=list[QuestionRequest], status_code=status.HTTP_201_CREATED)
async def crear_questions_endpoint(question: list[Question] = Body(...), current_user: dict = Depends(is_tercer_rango)):
    """
    Crea una o varias categorías en la base de datos.
    """
    nuevas_preguntas = service_questions.insertar_question(question, current_user)
    return nuevas_preguntas 

@router.get("/Ver/Todo", response_model=list[Question], status_code=status.HTTP_202_ACCEPTED)
async def view_old_categories(current_user: dict = Depends(is_primer_rango)):
    """
    End point encargado de mostrar todos los documentos de preguntas
    """
    preguntas = service_questions.visionar_todas_las_preguntas()
    return preguntas

@router.put("/Actualizar/Id", response_model=list[Question], status_code=status.HTTP_202_ACCEPTED)
async def actualizar_id(current_user: dict = Depends(is_primer_rango)):
    """
    End point que permite actualizar el id de str a Object id
    """
    service_questions.modificar_id()

@router.get("/Random/General", response_model=QuestionRequest, status_code=status.HTTP_202_ACCEPTED)
async def view_question_random(current_user: dict = Depends(get_current_user)):
    """
    End point que llama a una pregunta aleatoria en general.
    """
    question = service_questions.play_question_random()
    return question

@router.get("/Categoria/Principal/{categoria}", response_model=QuestionRequest, status_code=status.HTTP_202_ACCEPTED)
async def view_question_by_category(categoria:str, current_user: dict = Depends(get_current_user)):
    """
    End point el cual retorna una pregunta de una categoria determinada.
    Funciona con todas las categorias de cualquier grado.
    """
    question = service_questions.play_question_by_category(categoria)
    return question


@router.get("/Duelo/General", response_model=list[QuestionRequest], status_code=status.HTTP_202_ACCEPTED)
async def play_duel_general_router(current_user: dict = Depends(get_current_user)):
    """
    End point el cual retorna 10 preguntas para el duelo.
    """
    question = service_questions.play_duel_general()
    return question

@router.get("/Duelo/Categoria/{categoria}", response_model=list[QuestionRequest], status_code=status.HTTP_202_ACCEPTED)
async def play_duel_category_router(categoria:str, current_user: dict = Depends(get_current_user)):
    """
    End point encargado de devolveer 10 preguntas de una categoria.
    """
    question = service_questions.play_duel_category(categoria)
    return question

@router.patch("/Responder/Pregunta", response_model=RespuestaUsuario, status_code=status.HTTP_202_ACCEPTED)
async def aswer_question(respuesta:dict = Body(...), current_user: dict = Depends(get_current_user)):
    """
    End point para responder una pregunta.
    """
    question, usuario = service_questions.aswer_one_question(respuesta, current_user)
    
    return {"usuario": usuario, "respuesta": question}

@router.get("/Ver/Por/{id}", response_model=Question, status_code=status.HTTP_202_ACCEPTED)
async def view_for_id(id: str,  current_user: dict = Depends(is_segundo_rango)):
    """
    End point que sirve para visualizar una pregunta por medio de su id
    """
    pregunta = service_questions.view_question_for_id(id)
    return pregunta