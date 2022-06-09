from sqlalchemy.orm import Session
from . import models, schemas
import os
### USER CRUD ###

def get_user_by_id(session: Session, user_id: int):
	return session.query(models.User).filter_by(id=user_id).first()

def get_user_by_username(session: Session, username: str):
	return session.query(models.User).filter_by(username=username).first()

def get_users(session: Session, verified: bool = True, skip: int = 0, limit: int = 50):
	return session.query(models.User).filter_by(verified=verified).offset(skip).limit(limit).all()

def create_user(session: Session, user: schemas.UserCreate):
	db_user = models.User(**user.dict())
	session.add(db_user)
	session.commit()
	session.refresh(db_user)
	return db_user

def verify_user(session: Session, user_id: int):
	user = get_user_by_id(session, user_id)
	if user:
		user.verified = True
		session.commit()
	session.refresh(user)
	return user

def verify_users(session: Session, user_ids: list(int)):
	users = []
	for user_id in user_ids:
		user = verify_user(session, user_id)
		users.append(user)
	return users

def delete_user(session: Session, user_id: int):
	user = get_user_by_id(session, user_id)
	session.delete(user)
	session.commit()

### DEVICE CRUD ###

def get_device(session: Session, device_id: int):
	return session.query(models.Device).filter_by(id=device_id).first()

def get_device_by_name(session: Session, name: str):
	return session.query(models.Device).filter_by(name=name).first()

def get_devices(session: Session, verified: bool = True, skip: int = 0, limit: int = 50):
	return session.query(models.Device).filter_by(verified=verified).offset(skip).limit(limit).all()

def create_device(session: Session, device: schemas.DeviceCreate):
	db_device = models.Device(**device.dict())
	session.add(db_device)
	session.commit()
	session.refresh(db_device)
	return db_device

def verify_device(session: Session, device_id: int):
	device = get_device(session, device_id)
	if device:
		device.verified = True
		session.commit()
	session.refresh(device)
	return device

def verify_devices(session: Session, device_ids: list(int)):
	devices = []
	for device_id in device_ids:
		device = verify_device(session, device_id)
		devices.append(device)
	return devices

def delete_device(session: Session, device_id: int):
	device = get_device(session, device_id)
	session.delete(device)
	session.commit()

### FILE CRUD ###
def get_file(session: Session, file_id: int):
	return session.query(models.File).filter_by(id=file_id).first()

def create_file(session: Session, file: schemas.FileCreate, device_id: int):
	path = os.path.join(str(device_id), file.extension, file.filename)
	db_file = models.File(**file.dict(), local_path=path, device_id=device_id)
	session.add(db_file)
	session.commit()
	session.refresh(db_file)
	return db_file

def create_files(session: Session, files: list(schemas.FileCreate), device_id: int):
	files_lst = []
	for file in files:
		db_file = create_file(session, file, device_id)
		files_lst.append(File)
	return files_lst

def delete_files(session: Session, file_id):
	file = get_file(session, file_id)
	session.delete(file)
	session.commit()