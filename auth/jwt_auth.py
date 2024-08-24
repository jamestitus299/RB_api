import os
from dotenv import load_dotenv
import time
from typing import Dict
import jwt    

load_dotenv()

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

# returns the jwt token as json
def token_response(token: str):
    """
        returns the JWT token as a dict {"access_token": "token"}
    """
    return {
        "access_token": token
    }

# creates a jwt token based on the user id (email) passed
def sign_jwt(user_id: str) -> Dict[str, str]:
    """
        returns a JWT encoded with the user_id, as a dict {"access_token": "token"}
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 2 * 3600  # expiraton time
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token_response(token)


# decodes and validates the jwt token
def decode_jwt(token: str) -> dict:
    """
        returns a valid payload if the token is valid or None
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None

