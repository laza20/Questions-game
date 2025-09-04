from fastapi import FastAPI
from routers import (
    categorias,
    questions,
    usuarios
)


app = FastAPI()

app.include_router(categorias.router)
app.include_router(questions.router)
app.include_router(usuarios.router)