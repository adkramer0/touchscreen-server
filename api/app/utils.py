from datetime import datetime, timedelta
from jose import jwt
from .crud import get_user_by_username, get_device_by_name
from sqlalchemy.orm import Session
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
def authenticate_user(session: Session, username: str, password: str):
	user = get_user_by_username(session, username)
	if not user:
		return False 
	if not user.verify_password(password):
		return False
	return user
def authenticate_device(session: Session, name: str, password: str):
	device = get_device_by_name(session, name)
	if not device:
		return False 
	if not device.verify_password(password):
		return False
	return device

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def extract_protocols(filename):
	pass