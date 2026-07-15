from fastapi import FastAPI

from backend.database import Base, engine
import backend.models  # Registers every model with Base

app = FastAPI()

Base.metadata.create_all(bind=engine)