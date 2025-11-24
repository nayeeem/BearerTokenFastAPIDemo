from fastapi import APIRouter
from app.models.token import Token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from app.models.fakedb import get_db
from app.models.user import User, UserInDB
from app.models.utility import authenticate_user, get_user
from app.dependencies import get_current_active_user

router = APIRouter()


# Routes
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real app, generate a proper JWT token here
    access_token = user.username  # Using username as token for simplicity in this example
    return {"access_token": access_token, "token_type": "bearer"}


# Protected route to get current user
@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


# Protected route example
@router.get("/items/")
async def read_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"message": f"Hello {current_user.username}! Here are your items."}
