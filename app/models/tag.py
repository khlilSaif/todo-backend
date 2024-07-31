from sqlalchemy import Column, ForeignKey, Integer, String
from ..database import Base

class Tag(Base):
    __tablename__ = "tag"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=True)
    colorHash = Column(String, nullable=False)