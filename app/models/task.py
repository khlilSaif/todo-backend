from ..database import Base
from sqlalchemy import Column, Integer, String,ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = 'task'
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    project_id = Column(Integer, ForeignKey("project.id", ondelete='CASCADE'), nullable=False)
    description = Column(String, nullable=True)
    blocked_task = Column(Integer, ForeignKey("task.id"), nullable=True)
    tag_id = Column(Integer, (ForeignKey("tag.id")) ,nullable=True)
    completed = Column(Boolean, default= False, nullable= True)