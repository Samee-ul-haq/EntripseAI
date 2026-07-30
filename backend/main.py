from fastapi import FastAPI

from backend.database import Base, engine
import backend.models  # Registers every model with Base
from backend.routes import user, workspace

app = FastAPI(title="Enterprise AI Backend")


app.include_router(user)
app.include_router(workspace)


@app.get("/")
def root():
    return {"message": "Enterprise AI Backend API running"}

