from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base

class TaskBlockers(Base):
    __tablename__ = 'task_blockers'

    user_id = Column(ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey('task.id', ondelete='CASCADE'), primary_key=True)
    blocked_task_id = Column(Integer, ForeignKey('task.id', ondelete='CASCADE'), primary_key=True)