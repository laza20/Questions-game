from fastapi import FastAPI
from routers import (
    categorias
)


app = FastAPI()

app.include_router(categorias.router)