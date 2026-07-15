import bcrypt
from sqlalchemy import Column, Integer,  String
from sqlalchemy.orm import relationship

from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String,nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, null=False)

    workspace =  relationship("Workspace",back_populates= "user", cascade = "all, delete-orphan")

    @property
    def password(self):
        raise AttributeError("The password can not be read directly")
    
    @password.setter
    def password(self,plain_text_password : str):
        """Intercept raw password input and hash it automatically"""

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_text_password.encode("utf-8"),salt)

        self.password_hash = hashed_password
