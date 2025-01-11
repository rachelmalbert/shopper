from datetime import datetime
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select
from app import database as db
from app.schema import(
    UserInDB,
    UserRegistrationRequest
)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

#TODO: store key in os environment
JWT_KEY = os.environ.get("JWT_KEY", default="insecure-jwt-key-for-dev")
JWT_ALG = "HS256"
JWT_DURATION = 3600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db_dependency = Annotated[Session, Depends(db.get_session)]


class AccessTokenResponse(BaseModel):
    """
    Response model for returning the access token.

    This model is used to return the access token and its type (Bearer).
    """
    access_token: str
    token_type: str


# ------------------------------------- #
#              CREATE                   #
# ------------------------------------- #
@auth_router.post("/register")
def create_user(*, session: db_dependency, registration: UserRegistrationRequest):
    """
    Register a new user in the system.

    - **registration**: The user registration data (username, password).
    - **session**: The database session used to interact with the database.

    This endpoint registers a new user by saving the user details in the database, 
    including hashing the user's password using bcrypt.

    Returns:
        - The newly created user object (UserInDB).
    """

    new_user = UserInDB(
        **registration.model_dump(),
        hashed_password=pwd_context.hash(registration.password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@auth_router.post("/token", response_model=AccessTokenResponse)
def get_access_token(*, session: db_dependency, form: OAuth2PasswordRequestForm = Depends()):
    """
    Obtain an access token for an authenticated user.

    - **form**: The OAuth2 password request form, containing the username and password.
    - **session**: The database session used to verify the user.

    This endpoint authenticates the user using the provided username and password. 
    If authentication is successful, a JWT access token is generated and returned.
    
    Returns:
        - An access token and its type (Bearer).
    
    Raises:
        - 401 Unauthorized if the username or password is incorrect.
    """

    # Authenticate the user, return false if user can not be authenticated
    user = authenticate_user(session, form)
    if not user:
        raise HTTPException(status_code=401, detail="username or password is incorrect")
    
    # If user is authenticated, generate JWT access token
    token = create_access_token(user)
    return AccessTokenResponse(
        access_token=token,
        token_type="Bearer"
    )

# ------------------------------------- #
#              Helpers                  #
# ------------------------------------- #

def authenticate_user(session: Session, form: OAuth2PasswordBearer):
    """
    Authenticate the user by verifying the provided username and password.

    - **session**: The database session to query the user.
    - **form**: The OAuth2 password request form, containing the username and password.

    Returns:
        - The authenticated user object if credentials are valid.
        - False if authentication fails (incorrect username or password).
    """
    user = session.exec(select(UserInDB).where(UserInDB.username == form.username)).first()

    if not user: # user with the given username doesn't exist 
        return False 
    if not pwd_context.verify(form.password, user.hashed_password): # password is incorrect
        return False
    return user

def create_access_token(user: UserInDB):
    """
    Generate a JWT access token for the authenticated user.

    - **user**: The user object for which the token is created.

    Returns:
        - The generated JWT access token as a string.
    """
    expires = int(datetime.now().timestamp()) + JWT_DURATION
    payload = {'sub' : user.username, 'id' : user.id, 'exp' : expires}
    return jwt.encode(payload, key=JWT_KEY, algorithm=JWT_ALG)

def get_current_user(session: db_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieve the current authenticated user based on the provided JWT token.

    - **session**: The database session to query the user.
    - **token**: The JWT token extracted from the Authorization header.

    Returns:
        - The authenticated user object if the token is valid.
    
    Raises:
        - 401 Unauthorized if the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, key=JWT_KEY, algorithms=[JWT_ALG])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="could not validate user")
        user = session.get(UserInDB, user_id)
        print("!!", user)
        return  user
    except JWTError:
        raise HTTPException(status_code=401, detail="JWTError")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="expired signature")