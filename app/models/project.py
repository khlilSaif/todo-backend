from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default= False, nullable= False)
