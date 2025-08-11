from fastapi import FastAPI
from routers import (
    categorias,
    sub_categorias
)


app = FastAPI()

app.include_router(categorias.router)
app.include_router(sub_categorias.router)