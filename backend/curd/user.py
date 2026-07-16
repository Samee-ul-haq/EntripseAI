from backend.database import get_db
from backend.routes import create_user, get_user
from backend.models import User

db = get_db

create_user(db,User)

get_user(db, User)