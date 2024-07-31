from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from .. import schemas
from ..database import get_db
from .. import models
from .. import helpers

router = APIRouter(
    tags= ["Subtasks"],
    prefix = "/subtask"
)

@router.post('', response_model = list[schemas.SubTaskResponse])
async def getSubstasks(subtask_request: schemas.SubtaskIn, db: Session = Depends(get_db)):
    
    if not helpers.token.resolve_access_token(subtask_request.token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        substasks = db.query(models.Subtasks).filter(models.Subtasks.task_id == subtask_request.task_id).all()
        return ( substasks )
    except Exception as e:
        raise HTTPException(status_code=500, detail="There was an error getting the substasks") 

@router.post('/add', response_model=schemas.SubtaskOut)
async def add_subtask(subtask_request: schemas.Subtask, db: Session = Depends(get_db)):
    if not helpers.token.resolve_access_token(subtask_request.token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        subtask_data: schemas.Subtask = subtask_request
        subtask: models.Subtasks = models.Subtasks(
            task_id=subtask_data.task_id,
            description=subtask_data.description
        )
        db.add(subtask)
        db.commit()
        db.refresh(subtask)
        return schemas.SubtaskOut(
            id = subtask.id,
            description = subtask.description,
            message="Subtask Added Successfully",
            status=200
        )
    except Exception as e:
        db.rollback()
        return schemas.OurBaseModelOut(
            message="There was an error adding the subtask",
            status=500
        )


@router.post('/delete', response_model=schemas.OurBaseModelOut)
async def delete_subtask(subTask: schemas.task_to_delete, db: Session = Depends(get_db)):
    id =  helpers.token.resolve_access_token(subTask.token)
    if not id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        subtask = db.query(models.Subtasks).filter(models.Subtasks.id == subTask.task_id).first()
        if not subtask:
            raise HTTPException(status_code=404, detail="Subtask not found")
        db.delete(subtask)
        db.commit()
        return schemas.OurBaseModelOut(
            message='Subtask deleted successfully',
            status=200
        )
    except Exception as e:
        db.rollback()
        return schemas.OurBaseModelOut(
            message="There was an error deleting the subtask",
            status=500
        )

@router.put('/update', response_model=schemas.OurBaseModelOut)
async def update_subtask(subtask_request: schemas.UpdateSubtaskInput, db: Session = Depends(get_db)):
    id = helpers.token.resolve_access_token(subtask_request.token)
    if not id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        subtask = db.query(models.Subtasks).filter(models.Subtasks.id == subtask_request.subtask.id).first()
        if not subtask:
            raise HTTPException(status_code=404, detail="Subtask not found")
        subtask.description = subtask_request.subtask.description
        subtask.completed = subtask_request.subtask.completed
        db.add(subtask)
        db.commit()
        db.refresh(subtask)
        return schemas.OurBaseModelOut(
            status= 200,
            message="Subtask updated successfully",
        )
    except Exception as e:
        db.rollback()
        print(e)
        return schemas.OurBaseModelOut(
            message="There was an error updating the subtask",
            status=500
        )