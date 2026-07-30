from fastapi import FastAPI

from backend.database import Base, engine
import backend.models  # Registers every model with Base
from backend.routes import user, workspace, conversation, message

app = FastAPI(title="Enterprise AI Backend")


app.include_router(user.router)
app.include_router(workspace.router)
app.include_router(conversation.router)
app.include_router(message.router)


@app.get("/")
def root():
    return {"message": "Enterprise AI Backend API running"}

