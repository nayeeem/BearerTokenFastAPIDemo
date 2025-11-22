from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from fakedb import get_db

# Initialize FastAPI app
app = FastAPI()

# Initialize the fake users database
fake_users_db = get_db()


# Pydantic models
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# In a real application, replace this with a secure token generation and validation mechanism (e.g., JWT)
# and a proper user database.
class UserInDB(User):
    hashed_password: str
   
   
# Token model
class Token(BaseModel):
    access_token: str
    token_type: str


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Utility functions
def get_user(username: str):
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        # Unpacks **user_dict into UserInDB fields
        return UserInDB(hashed_password=user_dict["password"], **user_dict) 
    return None


# Authenticate user
def authenticate_user(username: str, password: str):
    user = get_user(username)
    # In this example both Password and HashedPassword are same.
    # In real app, verify hashed password properly.
    if not user or user.hashed_password != password:  
        return None
    return user


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


# Routes
@app.post("/token", response_model=Token)
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
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


# Protected route example
@app.get("/items/")
async def read_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {"message": f"Hello {current_user.username}! Here are your items."}