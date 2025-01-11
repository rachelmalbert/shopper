from fastapi import FastAPI
from contextlib import asynccontextmanager
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import create_db_and_tables
import app.utils as utils
import random

from app.routers.address import address_router
from app.routers.auth import auth_router
from app.routers.googleAPI import google_router
from app.routers.user import user_router

# Create database
# Called once at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(
    lifespan=lifespan,
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(address_router)
app.include_router(auth_router)
app.include_router(google_router)
app.include_router(user_router)

# ------------- #
#   DATABASE    #
# ------------- #


# ---------- #
#   ROUTES   #
# ---------- #


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

# Mangum handler to run FastAPI on Lambda
handler = Mangum(app)



