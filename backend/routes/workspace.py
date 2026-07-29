from fastapi import APIRouter
from sqlalchemy import orm
import jwt
import os



SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


