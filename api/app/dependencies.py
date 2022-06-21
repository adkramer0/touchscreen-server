from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, jws
import os
import motor.motor_asyncio
from sqlalchemy.orm import Session
from .data.database import SessionLocal
from . import crud, schemas
from .data.datastore import get_mongo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

async def get_fs():
    db = await get_mongo()
    fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
    return fs

async def user_authorized(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client = payload.get('sub')
        if client is None or client.split(':', 1)[0] != 'user':
            raise credentials_exception
        username = client.split(':', 1)[1]
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(session, username)
    if user is None:
        raise credentials_exception
    if not user.verified:
        raise HTTPException(status_code=400, detail="Unverified user")
    return user
async def device_authorized(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client = payload.get('sub')
        if client is None or client.split(':', 1)[0] != 'device':
            raise credentials_exception
        device_id = int(client.split(':', 1)[1])
    except JWTError:
        raise credentials_exception
    device = crud.get_device(session, schemas.DeviceID(id=device_id))
    if device is None:
        raise credentials_exception
    if not device.verified:
        raise HTTPException(status_code=400, detail="Unverified device")
    return schemas.DeviceID(id=device.id)