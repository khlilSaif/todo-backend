from sqlalchemy import Column, String, Integer, ForeignKey
from ..database import Base

class User(Base):  
    # TODO add foreign key for blocked tasks 
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)