from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, update, delete
from ..database import get_db 
from .. import models
from .. import schemas
from .. import helpers

router = APIRouter(
    tags= ["Tasks"],
    prefix = "/task"
)

@router.post('', response_model = list[schemas.tasksOut])
async def get_tasks(task_request: schemas.task_request, db: Session = Depends(get_db)):
    try:
        if not helpers.token.resolve_access_token(task_request.token):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        tasks = db.query(models.Task).filter(models.Task.project_id == task_request.project_id).all()
        return ( tasks )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="There was an error getting the tasks")

@router.post('/add', response_model=schemas.tasksOut)
async def add_task(task_request_add: schemas.task_request_add, db: Session = Depends(get_db)):
    id = helpers.token.resolve_access_token(task_request_add.token)
    if not id:
        return schemas.OurBaseModelOut(
            message="Invalid Token",
            status= 401
        )
    try:
        task_data = task_request_add.task

        task_to_add = models.Task(
            project_id=task_data.project_id,
            description=task_data.description,
            blocked_task=task_request_add.blocked_task
        )
        db.add(task_to_add)
        db.flush()
        db.refresh(task_to_add)

        if task_request_add.blocked_task:
            blocked_task_data = task_request_add.blocked_task
            blocked_task = models.TaskBlockers(task_id=task_to_add.id, blocked_task_id=blocked_task_data, user_id= id)
            db.add(blocked_task)
            db.flush()
            db.refresh(blocked_task)
            task_blocked = db.query(models.TaskBlockers).all()
            task_blocked_pairs = [(i.task_id, i.blocked_task_id) for i in task_blocked]
            graph = create_graph(task_blocked_pairs)
            if not task_could_be_added(graph, set(), blocked_task_data):
                db.rollback()
                return schemas.OurBaseModelOut(
                    message="You can't add this task please check your dependencies",
                    status=405
                )

        db.commit()
        return task_to_add
    except Exception as e:
        db.rollback()
        print(e) # for debugging 
        return schemas.OurBaseModelOut(
            message="There was an error adding the task",
            status=500
        )
    
def create_graph(edges):
    graph = {}
    for i in edges:
        if i[0] not in graph:
            graph[i[0]] = []
        graph[i[0]].append(i[1])

    return graph

def task_could_be_added(graph, visited, curr):
    if curr in visited:
        return False

    visited.add(curr)

    if curr not in graph:
        return True
    
    for neighbor in graph[curr]:
        if not task_could_be_added(graph, visited, neighbor):
            return False

    return True

@router.post('/delete', response_model=schemas.OurBaseModelOut)
async def delete_task(task_to_be_deleted: schemas.task_to_delete, db: Session = Depends(get_db)):
    try:
        user_id = helpers.token.resolve_access_token(task_to_be_deleted.token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    
        task = db.query(models.Task).filter(models.Task.id == task_to_be_deleted.task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.execute(
            update(models.Task).where(models.Task.blocked_task == task_to_be_deleted.task_id).values(blocked_task=None)
        )
        db.delete(task)
        db.commit()
        return schemas.OurBaseModelOut(
            message='Task deleted successfully',
            status=200
        )
    except Exception as e:
        db.rollback()
        print(e)
        return schemas.OurBaseModelOut(
            message="There was an error deleting the task",
            status=500
        )

@router.put('/update', response_model=schemas.OurBaseModelOut)
async def update_task(task_request: schemas.taskUpdateInput, db: Session = Depends(get_db)):
    try:
        user_id = helpers.token.resolve_access_token(task_request.token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        task = db.query(models.Task).filter(models.Task.id == task_request.task.id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task.description = task_request.task.description
        task.completed = task_request.task.completed
        task.blocked_task = task_request.task.blocked_task
        if( task_request.task.blocked_task ):
            db.execute(
                delete(models.TaskBlockers).where(and_(models.TaskBlockers.task_id == task.id, models.TaskBlockers.blocked_task_id == task_request.task.blocked_task))
            )
            if task_request.task.blocked_task is not None:
                blocked_task_data = task_request.task.blocked_task
                blocked_task = models.TaskBlockers(task_id=task.id, blocked_task_id=blocked_task_data, user_id=user_id)
                db.add(blocked_task)
                db.flush()
                db.refresh(blocked_task)
                task_blocked = db.query(models.TaskBlockers).filter(models.TaskBlockers.user_id == user_id).all()
                task_blocked_pairs = [(i.task_id, i.blocked_task_id) for i in task_blocked]
                graph = create_graph(task_blocked_pairs)
                if not task_could_be_added(graph, set(), blocked_task_data):
                    db.rollback()
                    return schemas.OurBaseModelOut(
                        message="You can't add update this task please check your dependencies",
                        status=405
                    )
            
        db.add(task)
        db.commit()
        db.refresh(task)
        return schemas.OurBaseModelOut(
            status= 200,
            message="Task updated successfully",
        );
    except Exception as e:
        db.rollback()
        print(e)
        return schemas.OurBaseModelOut(
            message="There was an error updating the task",
            status=500
        )

@router.post('/assignTagToTask/{taskId}/{tagId}', response_model = schemas.task)
async def assignTagToTask(tagInput: schemas.tagInput, taskId: int, tagId: int, db: Session = Depends(get_db)):
    try:
        id = helpers.token.resolve_access_token(tagInput.token)
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        task = db.query(models.Task).filter(models.Task.id == taskId).first()
        task.tag_id = tagId
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="internal server error")
