from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from routers import (
    categorias,
    questions,
    usuarios,
    preguntas_respondidas_user,
    logros
)
from dependencies import auth_dependencies


app = FastAPI()

app.include_router(categorias.router)
app.include_router(questions.router)
app.include_router(usuarios.router)
app.include_router(auth_dependencies.router)
app.include_router(preguntas_respondidas_user.router)
app.include_router(logros.router)