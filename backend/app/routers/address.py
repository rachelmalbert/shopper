from typing import Annotated
from app.routers.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app import utils
from app.schema import (UserInDB, AddressRequest, AddressInDB)
from app import database as db

address_router = APIRouter(prefix="/address", tags=["Address"])

STORES = [
    { "name": "Giant", "address": "1234 Road", "city": "Philadelphia", "zip": 19020 },
    { "name": "Whole Foods", "address": "5678 Market St", "city": "Philadelphia", "zip": 19103 },
    { "name": "Trader Joe's", "address": "9875 Chestnut St", "city": "Philadelphia", "zip": 19107 },
    { "name": "Target", "address": "2345 Roosevelt Blvd", "city": "Philadelphia", "zip": 19152 },
    { "name": "Acme Markets", "address": "6789 Adams Ave", "city": "Philadelphia", "zip": 19111 },
    { "name": "Walmart", "address": "4321 South St", "city": "Philadelphia", "zip": 19146 },
    { "name": "CVS Pharmacy", "address": "8765 Pine St", "city": "Philadelphia", "zip": 19103 },
    { "name": "Rite Aid", "address": "1357 Broad St", "city": "Philadelphia", "zip": 19107 },
    { "name": "Lidl", "address": "2468 Levick St", "city": "Philadelphia", "zip": 19149 },
    { "name": "Best Buy", "address": "1359 City Ave", "city": "Philadelphia", "zip": 19151 }
]


user_dependency = Annotated[UserInDB, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(db.get_session)]

# ------------------------------------- #
#               POST                    #
# ------------------------------------- #

@address_router.post("/post")
def create_address(session: db_dependency, user: user_dependency, address: AddressRequest):
    """
    Create a new Address and associate it with the authenticated user.

    - **address**: The address details.
    - **user**: The authenticated user, obtained through the `get_current_user` dependency.

    Returns the newly created Address object.
    """
    new_address = AddressInDB(**address.model_dump(), user_id=user.id)
    session.add(new_address)
    session.commit()
    session.refresh(new_address)
    return new_address

@address_router.post("/stores")
def add_stores(session: db_dependency, user: user_dependency):
    """
    Add a predefined list of stores to the authenticated user's account.

    - **user**: The authenticated user, obtained through the `get_current_user` dependency.

    Iterates over the predefined `STORES` list and creates a new address entry for each store.
    Returns no content (status 204) upon successful execution.
    """
    for store in STORES:
        new_address = AddressInDB(user_id=user.id, name=store["name"], address=store["address"], city=store["city"], state="PA", zip=store["zip"])
        session.add(new_address)
        session.commit()
        session.refresh(new_address)


# ------------------------------------- #
#                 GET                   #
# ------------------------------------- #

@address_router.get("/get/all")
def get_addresses(session: db_dependency, user: user_dependency):
    """
    Get all Addresses belonging to the authenticated user.

    - **user**: The authenticated user, obtained through the `get_current_user` dependency.

    Returns a list of AddressInDB objects for the current user, or `None` if no addresses are found.
    """
    query = select(AddressInDB).where(AddressInDB.user_id==user.id)
    addresses = session.exec(query).all()
    if len(addresses) == 0:
        return None
    return addresses

@address_router.get("/get/{address_id}")
def get_address(session: db_dependency, address_id: int):
    """
    Get a specific Address by its ID.

    - **address_id**: The ID of the address to retrieve.

    Returns the AddressInDB object for the given address ID.
    """
    address = db.get_address(session, address_id)
    return address

@address_router.get("/add/{distance}/{lat}/{long}")
def add_distance(lat: float =40.13201011242109, long: float = -74.93605191591041, distance: int = 4):
    """
    Calculate a new set of coordinates by adding a specified distance (in miles) to a given latitude/longitude.

    - **lat**: Latitude of the starting point (default is 40.132).
    - **long**: Longitude of the starting point (default is -74.936).
    - **distance**: The distance to add in miles (default is 4 miles).

    Returns the new coordinates (latitude and longitude) after applying the distance.
    """
    new_coords = utils.add_distance(lat, long, distance)
    return new_coords   

# ------------------------------------- #
#                 DELETE                #
# ------------------------------------- #

@address_router.delete("/delete/{address_id}")
def delete_address(session: db_dependency, user: user_dependency, address_id: int):
    """
    Delete an Address associated with the authenticated user.

    - **address_id**: The ID of the address to delete.
    - **user**: The authenticated user, used to verify the user owns the address.

    Returns a message confirming the deletion of the address.
    """
    delete = db.get_address(session, address_id)
    session.delete(delete)
    session.commit()
    return f"Deleted address with id {address_id}"
 

