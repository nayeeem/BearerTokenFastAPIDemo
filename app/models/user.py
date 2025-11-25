from pydantic import BaseModel

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
   