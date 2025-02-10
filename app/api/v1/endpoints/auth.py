from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import datetime
import os

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

@router.post("/login")
def login():
    """
    This function generates a JWT token for user authentication.

    Parameters:
    None

    Returns:
    dict: A dictionary containing the generated JWT token under the key "access_token".
    """
    expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({"exp": expiration}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}

@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    """
    This function verifies the JWT token provided in the request header and returns a message along with the token expiration time.

    Parameters:
    token (str): The JWT token provided in the request header. This parameter is optional and will be injected by the FastAPI Depends function.

    Returns:
    dict: A dictionary containing a "message" indicating the validity of the token and the token expiration time under the key "exp".

    Raises:
    HTTPException: If the token is expired or invalid, an HTTPException will be raised with the appropriate status code and error message.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"message": "Valid token!", "exp": payload["exp"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
