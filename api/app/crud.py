from sqlalchemy.orm import Session
from . import models, schemas

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
	return session.query(models.Device).filter_by(id=dev_id).first()

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

def verify_users(session: Session, device_ids: list(int)):
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

def create_file(session: Session, file: schemas.FileCreate, path: str, device_id: int):
	db_file = models.File(**file.dict(), local_path=path, device_id=device_id)
	
def create_files():
	pass
def delete_files():
	pass