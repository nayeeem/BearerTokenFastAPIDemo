from fastapi import APIRouter
from app.models.token import Token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from app.models.fakedb import get_db
from app.models.user import User, UserInDB
from app.models.utility import authenticate_user, get_user

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # In a real app, decode and validate the token (e.g., JWT)
    # and extract user information. For this example, we'll just use the token as the username.
    user = get_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# Dependency to get current active user
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

