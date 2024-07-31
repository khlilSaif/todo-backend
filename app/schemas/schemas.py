from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True #Retrieving and validating data from the database using Pydantic's ORM mode
     
class OurBaseModelOut(OurBaseModel): #We want to return classes with message and status
    message: Optional[str]
    status: Optional[int]

class task(OurBaseModel):
    project_id: Optional[int] = None
    description: Optional[str] = None 
    tag_id: Optional[int] = None
    

class tasksOut(task):
    id: int
    blocked_task: Optional[int] = None
    completed: Optional[bool] = None

class task_request(task):
    token: Optional[str]

class tag(OurBaseModel):
    id: Optional[int]
    name: Optional[str]
    user_id: Optional[int]
    colorHash: Optional[str]
    
class task_request_add(OurBaseModel):
    task: Optional[task]
    blocked_task: Optional[int] = None
    token: Optional[str] = None
    
class task_request_update(tasksOut):
    token: Optional[str]
    

class taskUpdate(OurBaseModel):
    id: Optional[int]
    description: Optional[str]
    completed: Optional[bool] = None
    tag_id: Optional[int] = None 
    blocked_task: Optional[int] = None
    project_id: Optional[int] = None
    
class taskUpdateInput(OurBaseModel):
    task: Optional[taskUpdate]
    token: Optional[str] = None
    
class project(OurBaseModel):
    name: Optional[str]
    description:  Optional[str]
    token: Optional[str]

class ProjectResponse(OurBaseModel):
    name: Optional[str]
    description: Optional[str]
    user_id: Optional[int]

class ProjectResponseOut(ProjectResponse):
    id: Optional[int]
    
class ProjectOut(OurBaseModelOut):
    id: Optional[int]

class User(OurBaseModel):
    username: Optional[str]
    password: Optional[str]
    
class UserIn(User):
    pass

class UserOut(User):
    pass

class Subtask(OurBaseModel):
    task_id: Optional[int]
    description: Optional[str]
    token: Optional[str]
    completed: Optional[bool] = None

class SubTask2(OurBaseModel):
    id: Optional[int]
    task_id: Optional[int]
    description: Optional[str]
    completed: Optional[bool] = None

class UpdateSubtaskInput(OurBaseModel):
    subtask: Optional[SubTask2]
    token: Optional[str] = None

class SubtaskUpdate(Subtask):
    id: Optional[int]
    
class SubtaskIn(OurBaseModel):
    task_id: Optional[int]
    token: Optional[str]
    
class SubTaskResponse(OurBaseModel):
    description: Optional[str]
    id: Optional[int]
    task_id: Optional[int]
    completed: Optional[bool] = None
    
class SubtaskOut(OurBaseModelOut):
    id: Optional[int]
    description: Optional[str] = None
    
class tagInput(OurBaseModel):
    token: Optional[str]

class tag_request(tagInput):
    name: Optional[str]

class UserLoginOut(OurBaseModelOut):
    access_token: Optional[str]
    token_type: Optional[str]
    
class task_to_delete(OurBaseModel):
    token: Optional[str]
    task_id: Optional[int]

class update_task_input(OurBaseModel):
    task: Optional[task]
    token: Optional[str]