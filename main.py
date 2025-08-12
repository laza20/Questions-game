from fastapi import FastAPI
from routers import (
    categorias,
    sub_categorias,
    micro_categorias,
    nano_categorias
)


app = FastAPI()

app.include_router(categorias.router)
app.include_router(sub_categorias.router)
app.include_router(micro_categorias.router)
app.include_router(nano_categorias.router)