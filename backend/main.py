from fastapi import FastAPI

from backend.database import Base, engine
import backend.models  # Registers every model with Base
from backend.routes.user import router as user_router

app = FastAPI()
app.include_router(user_router)

Base.metadata.create_all(bind=engine)