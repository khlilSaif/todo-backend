from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from .. import schemas, models
from ..database import get_db
from .. import helpers

router = APIRouter(
    tags= ["User"],
    prefix= "/user"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"An error occurred: {e}")

@router.post("/login", response_model=schemas.UserLoginOut)
def login(user: schemas.UserIn, response: Response, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if not db_user:
            raise HTTPException(status_code=400, detail="Incorrect username")
        
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        
        access_token = helpers.token.create_access_token(data={"user_id": db_user.id, "iad": datetime.utcnow().timestamp()})
        access_token_expires = timedelta(days=3)
        
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=access_token_expires.total_seconds())
        
        user_login_out = schemas.UserLoginOut(
            access_token=access_token,
            token_type="bearer",
            message="Login successful",
            status=200
        )
        return schemas.UserLoginOut(**user_login_out.dict())
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/signup", response_model= schemas.UserOut)
def signup(user: schemas.UserIn, db: Session = Depends(get_db)):
    try: 
        username_in_db = db.query(models.User).filter(models.User.username == user.username).first()
        print(user.username)
        print(user.password)
        if username_in_db is not None:
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = pwd_context.hash(user.password)
        user_to_add = models.User(**user.dict(exclude={"password"}), password=hashed_password)
        db.add(user_to_add)
        db.flush()
        db.commit()
        print("User added successfully")  # Added this line for debugging
        return user
    except Exception as error: 
        db.rollback()
        raise HTTPException(status_code=400, detail=str(error)) from error
