from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from .database import SessionLocal
from .crud import get_user_by_username, get_device
from .schemas import User, Device
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

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
    user = get_user_by_username(session, username)
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
        device_id = client.split(':', 1)[1]
    except JWTError:
        raise credentials_exception
    device = get_device(session, device_id)
    if device is None:
        raise credentials_exception
    if not device.verified:
        raise HTTPException(status_code=400, detail="Unverified device")
    return device