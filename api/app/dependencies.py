from fastapi import Depends, HTTPException, status, Request, WebSocket
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
import os
import motor.motor_asyncio
from sqlalchemy.orm import Session
from .data.database import SessionLocal
from . import crud, schemas
from .data.datastore import get_gridfs


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(self, tokenUrl, scheme_name: str = None, scopes: dict = {}, auto_error: bool = True):
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        req = request or websocket
        if req == None:
            return None

        authorization: str = req.cookies.get('Authorization')
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error and request != None: # only throw exception if request, not websocket
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param



class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="token", scopes={'user': 'user', 'device': 'device'})

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

async def get_fs():
    db = await get_gridfs()
    fs = motor.motor_asyncio.AsyncIOMotorGridFSBucket(db)
    return fs
async def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
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
    return user
    
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