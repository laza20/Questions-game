from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from db.client import db_client
from service.service_usuarios import oauth2

# Defines the scheme for getting the token from the header
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY")

class TokenData(BaseModel):
    username: str | None = None

# This is the function that validates the token
async def get_current_user(token: str = Depends(oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # payload = jwt.decode(token, hex_token, algorithms=[ALGORITHM])
        # Note: Be sure to use a persistent secret key, not one generated on each startup
        payload = jwt.decode(token, SECRET_KEY ,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # You might want to find the user in the database here to ensure they exist and are active
    user_in_db = db_client.Usuarios.find_one({"nombre_usuario": token_data.username})
    if user_in_db is None:
        raise credentials_exception

    return user_in_db


def is_primer_rango(current_user: dict = Depends(get_current_user)):
    if current_user["rango"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción."
        )
    
    return current_user

def is_segundo_rango(current_user: dict = Depends(get_current_user)):
    if current_user["rango"] != "Editor" and current_user["rango"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción."
        )
    
    return current_user

def is_tercer_rango(current_user: dict = Depends(get_current_user)):
    if current_user["rango"] != "Moderador" and current_user["rango"] != "Editor" and current_user["rango"] != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción."
        )
    
    return current_user