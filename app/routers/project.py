from fastapi import APIRouter, Depends, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session 
from .. import schemas
from .. import helpers
from .. import models

router = APIRouter( 
    tags= ["Projects"],
    prefix= '/project'
)
@router.post('/all', response_model= list[schemas.ProjectResponseOut])
async def get_all_projects(user_token: schemas.tagInput, db: Session = Depends(get_db)):
    try: 
        user_id = helpers.token.resolve_access_token(user_token.token)
        projects = db.query(models.Project).filter(models.Project.user_id == user_id).all()
        
        return projects
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="internal server error")
    
@router.post('/add', response_model= schemas.ProjectResponseOut)
async def add_project(project: schemas.project,db: Session = Depends(get_db)):
    try:
        user_id = helpers.token.resolve_access_token(project.token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        project_to_add = models.Project(user_id = user_id, name= project.name, description= project.description)
        db.add(project_to_add)
        db.flush()
        db.commit()
        db.refresh(project_to_add)
        return project_to_add
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="There was an error adding the project")
    
@router.post('/delete', response_model=schemas.OurBaseModelOut)
async def delete_project(project: schemas.task_to_delete ,db: Session = Depends(get_db)):
    try:
        
        if not helpers.token.resolve_access_token(project.token):
            raise HTTPException(status_code=401, detail="Unauthorized")

        project = db.query(models.Project).filter(models.Project.id == project.task_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        db.delete(project)
        db.commit()

        return schemas.OurBaseModelOut(
            message='Project and related tasks deleted successfully',
            status=200
        )
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="There was an error deleting the project and related tasks")

@router.put('/{id}', response_model=schemas.ProjectResponseOut)
async def update_project(id: int, project: schemas.project, db: Session = Depends(get_db)):
    try:
        if not helpers.token.resolve_access_token(project.token):
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        project_to_update = db.query(models.Project).filter(models.Project.id == id).first()
        if not project_to_update:
            raise HTTPException(status_code=404, detail="Project not found")
        project_to_update.name = project.name
        project_to_update.description = project.description
        db.commit()
        db.refresh(project_to_update)
        
        return project_to_update
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="There was an error updating the project")