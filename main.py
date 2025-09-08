from fastapi import FastAPI
from routers import (
    categorias,
    questions,
    usuarios
)
from dependencies import auth_dependencies


app = FastAPI()

app.include_router(categorias.router)
app.include_router(questions.router)
app.include_router(usuarios.router)
app.include_router(auth_dependencies.router)