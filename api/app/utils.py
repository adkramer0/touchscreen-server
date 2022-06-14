from datetime import datetime, timedelta
from jose import jwt
from .crud import get_user_by_username, get_device_by_name
from sqlalchemy.orm import Session
import os
import shutil
import pyclbr
SECRET_KEY = os.environ.get('SECRET_KEY')

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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt

async def save_protocols(files):
	files_ret = []
	for file in files:
		with open(file.filename, 'wb') as f:
			shutil.copyfileobj(file.file, f)
		files_ret.append(file.filename)
	return files_ret


def get_extension(filename: str):
	extension = filename.split('.', 1)[1]
	return extension

async def extract_protocols(filename: str):
	file = filename.split('.', 1)[0] # get files name without path, and without extension
	module = pyclbr.readmodule(file) # load info on all classes in file
	protocols = []
	for k, v in module: # check if base class is Protocol in all classes
		for v.super in v:
			if v == 'Protocol':
				protocols.append(k)
	return protocols

async def chunk_generator(grid_out):
	while True:
		chunk = await grid_out.readchunk()
		if not chunk:
			break
		yield chunk
		break


