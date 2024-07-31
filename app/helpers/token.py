from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt

SECRET_KEY = "e514dac6502a94621003329eaf689659a79377c5e11ac80e8e1d8e3df6135e13"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3


def create_access_token(data: dict):
    expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def resolve_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return id
    except JWTError as e:
        raise HTTPException(status_code=401, detail=str(e))
