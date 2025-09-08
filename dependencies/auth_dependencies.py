from fastapi import APIRouter, Depends
from dependencias import get_current_user # Import the function

router = APIRouter(prefix="/auth",
                   tags=["AUTH"],
                   responses={404:{"Message":"No encontrado"}}
)

@router.get("/my-items/")
async def read_my_items(current_user: dict = Depends(get_current_user)):
    # This code will only run if get_current_user successfully validates the token.
    return {"message": f"Hello, {current_user['nombre_usuario']}! Here are your items."}