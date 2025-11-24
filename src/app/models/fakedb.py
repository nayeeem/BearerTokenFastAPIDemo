# In a real application, replace this with a secure token generation and validation mechanism (e.g., JWT)
# and a proper user database.
fake_users_db = {
    "john": {
        "username": "john",
        "password": "12345678",  # In production, store hashed passwords
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "disabled": False,
    },
    "jane.smith": {
        "username": "jane.smith",
        "password": "password123",
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "disabled": True,
    },
    "elon.musk": {
        "username": "elon",
        "password": "123456",
        "full_name": "Elon Musk",
        "email": "elon.musk@example.com",
        "disabled": True,
    },
    "caroline": {
        "username": "caroline",
        "password": "123456",
        "full_name": "Caroline",
        "email": "caroline@example.com",
        "disabled": True,
    },
    "nicole": {
        "username": "nicole",
        "password": "123456",
        "full_name": "Nicole Smith",
        "email": "nicole@example.com",
        "disabled": True,
    },
}

# Function to get the fake users database
def get_db():
    return fake_users_db




