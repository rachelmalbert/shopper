from typing import Annotated
from app.routers.auth import get_current_user
from fastapi import APIRouter, Depends
from requests import Session

from app import database as db
from app.schema import (UserInDB, UserRegistrationRequest)

user_router = APIRouter(prefix="/user", tags=["User"])

user_dependency = Annotated[UserInDB, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(db.get_session)]


@user_router.get("/self", response_model=UserInDB)
def get_self(user: user_dependency):
    """
    Get the current authenticated user's details.

    This endpoint retrieves the details of the currently authenticated user based on the token provided.
    It uses the `get_current_user` dependency to ensure that the user is authenticated. If the user is found, 
    their information is returned.

    - **user**: The authenticated user object retrieved from the `get_current_user` dependency.

    Returns:
        - A `UserInDB` object containing the user's details, such as username, email, etc.

    Raises:
        - HTTPException with status code 401 if the user is not authenticated (handled by `get_current_user`).
    """
    if user:
        return user
    
    
  
