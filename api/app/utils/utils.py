from datetime import datetime, timedelta
from jose import jwt
from .. import crud, schemas
from sqlalchemy.orm import Session
import os
import shutil
import pyclbr
from ..data import database


SECRET_KEY = os.environ.get('SECRET_KEY')

async def authenticate_user(session: Session, username: str, password: str):
	user = crud.get_user_by_username(session, username)
	if not user:
		return False 
	if not user.verify_password(password):
		return False
	return user

async def authenticate_device(session: Session, device_id: schemas.DeviceID, password: str):
	device = crud.get_device(session, device_id)
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
        expire = datetime.utcnow() + timedelta(minutes=720) # 12 hours
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt

async def save_protocols(files):
	for file in files:
		with open('tmp_'+file.filename, 'wb') as f:
			shutil.copyfileobj(file.file, f)
		await file.seek(0)

async def delete_protocols(files):
	for file in files:
		filename = 'tmp_' + file.filename
		if os.path.exists(filename):
			os.remove(filename)


async def extract_protocols(filename: str):
	file = 'tmp_' + filename.split('.', 1)[0] # get files name without path, and without extension
	module = pyclbr.readmodule(file) # load info on all classes in file
	protocols = []
	for k, v in module.items(): # check if base class is Protocol in all classes
		for base in v.super:
			if base == 'Protocol':
				protocols.append(k)
	return protocols



def init_db():
	session = database.SessionLocal()
	SUPER_USER = 'admin'
	SUPER_PASSWORD = 'admin'
	SUPER_EMAIL = 'admin@domain.tld'
	verified_length = len(crud.get_users(session, True))
	if verified_length == 0:
		admin_schema = schemas.UserCreate(username=SUPER_USER, password=SUPER_PASSWORD, email=SUPER_EMAIL)
		admin_unverified = crud.create_user(session, admin_schema)
		admin = crud.verify_user(session, schemas.UserID(id=admin_unverified.id))
	elif verified_length > 1:
		admin = crud.get_user_by_username(session, SUPER_USER)
		if admin:
			crud.delete_user(session, schemas.UserID(id=admin.id))
	session.close()

