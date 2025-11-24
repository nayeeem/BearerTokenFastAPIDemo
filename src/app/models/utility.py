from app.models.fakedb import get_db
from app.models.user import UserInDB

# Initialize the fake users database
fake_users_db = get_db()

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



