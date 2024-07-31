import random
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from sqlalchemy import update
from sqlalchemy.orm import Session
from .. import models
from .. import helpers

router = APIRouter(
    tags = ["Tags"],
    prefix= "/tag"
)

@router.post('', response_model = list[schemas.tag])
async def getTag(tagInput: schemas.tagInput, db: Session = Depends(get_db)):
    try:
        id = helpers.token.resolve_access_token(tagInput.token)
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        tag = db.query(models.Tag).filter(models.Tag.user_id == id).all()
        
        return tag
    except Exception as e:
        raise HTTPException(status_code=500, detail="internal server error")

@router.post('/add', response_model = schemas.tag)
async def addTag(tagInput: schemas.tag_request, db: Session = Depends(get_db)):
    try:
        id = helpers.token.resolve_access_token(tagInput.token)
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        tag = models.Tag(name=tagInput.name, colorHash= generate_random_color(), user_id= id)
        db.add(tag)
        db.commit()
        db.refresh(tag)
        return tag
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="internal server error")

def generate_random_color():
    def is_dark(color):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        # Using a luminance formula to determine if the color is dark
        luminance = (0.299*r + 0.587*g + 0.114*b) / 255
        return luminance < 0.5

    while True:
        color = '#%06x' % random.randint(0, 0xFFFFFF)
        if not is_dark(color):
            return color
  
@router.post("/delete", response_model=schemas.OurBaseModelOut)
async def delete(tag :schemas.task_to_delete, db: Session = Depends(get_db)):
    try:
        id = helpers.token.resolve_access_token(tag.token)
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        tag_instance = db.query(models.Tag).filter(models.Tag.id == tag.task_id).first()
        if not tag_instance:
            raise HTTPException(status_code=404, detail="Tag not found")

        db.execute(
            update(models.Task).where(models.Task.tag_id == tag_instance.id).values(tag_id=None)
        )
        db.delete(tag_instance)
        db.commit()
        return schemas.OurBaseModelOut(
            message='Tag deleted successfully',
            status=200
        )
    except SQLAlchemyError as e:  
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="There was an error deleting the tag")

