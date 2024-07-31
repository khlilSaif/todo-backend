from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from ..database import Base
from sqlalchemy.orm import relationship

class Subtasks(Base):
    __tablename__ = 'subtasks'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    task_id = Column(Integer, ForeignKey("task.id", ondelete='CASCADE'), nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default= False, nullable= True)