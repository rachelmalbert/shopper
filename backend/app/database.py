from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
import os

from app.schema import (AddressInDB)


# Create the engine and database 
engine = create_engine(
    "sqlite:///app/database.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    """
    Creates the database tables based on the defined SQLModel schemas.

    Returns:
        None.
    """
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Provides a database session for interacting with the database.

    Returns:
        - A `Session` object that represents the database session.
    """
    with Session(engine) as session:
        yield session


def get_address(session: Session, address_id: int):
    """
    Retrieves an address from the database by its ID.

    - **session**: The database session used to interact with the database.
    - **address_id**: The ID of the address to retrieve from the database.

    Returns:
        - The `AddressInDB` object representing the address with the specified ID.

    Raises:
        - `HTTPException`: If the address with the given `address_id` does not exist, 
          a 404 HTTPException is raised with a detailed error message.
    """
    address = session.get(AddressInDB, address_id)
    if address:
        return address
    raise HTTPException(status_code=404, detail=f"Address with id of {address_id} not found")
