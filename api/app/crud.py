from sqlalchemy.orm import Session
from . import schemas
from .data import models
import os
### USER CRUD ###

def get_user_by_id(session: Session, user: schemas.UserID):
	return session.query(models.User).filter_by(**user.dict()).first()

def get_user_by_username(session: Session, username: str):
	return session.query(models.User).filter_by(username=username).first()

def get_users(session: Session, verified: bool = False):
	return session.query(models.User).filter_by(verified=verified).all()

def create_user(session: Session, user: schemas.UserCreate):
	db_user = models.User(**user.dict())
	session.add(db_user)
	session.commit()
	session.refresh(db_user)
	return db_user

def verify_user(session: Session, user_id: schemas.UserID):
	user = get_user_by_id(session, user_id)
	if user:
		user.verified = True
		session.commit()
	session.refresh(user)
	return user

def verify_users(session: Session, user_ids: list[schemas.UserID]):
	users = []
	for user_id in user_ids:
		user = verify_user(session, user_id)
		users.append(user)
	return users

def delete_user(session: Session, user: schemas.UserID):
	user = get_user_by_id(session, user)
	session.delete(user)
	session.commit()

### DEVICE CRUD ###

def get_device(session: Session, device: schemas.DeviceID):
	return session.query(models.Device).filter_by(**device.dict()).first()


def get_devices(session: Session, verified: bool):
	return session.query(models.Device).filter_by(verified=verified).all()

def create_device(session: Session, device: schemas.DeviceCreate):
	db_device = models.Device(**device.dict())
	session.add(db_device)
	session.commit()
	session.refresh(db_device)
	return db_device

def verify_device(session: Session, device_id: schemas.DeviceID):
	device = get_device(session, device_id)
	if device:
		device.verified = True
		session.commit()
	session.refresh(device)
	return device

def verify_devices(session: Session, device_ids: list[schemas.DeviceID]):
	devices = []
	for device_id in device_ids:
		device = verify_device(session, device_id)
		devices.append(device)
	return devices

def set_device_name(session: Session, id: int, name: str):
	device = get_device(session, schemas.DeviceID(id=id))
	if device:
		device.name = name 
		session.commit()
	session.refresh(device)
	return device
	
def delete_device(session: Session, device: schemas.DeviceID):
	device = get_device(session, device)
	session.delete(device)
	session.commit()

### FILE CRUD ###
def get_file(session: Session, file_id: int):
	return session.query(models.File).filter_by(id=file_id).first()

def get_files(session: Session, device: schemas.DeviceID):
	return session.query(models.File).filter_by(device_id=device.id).all()

def create_file(session: Session, file: schemas.FileCreate, device: schemas.DeviceID):
	db_file = models.File(**file.dict(), device_id=device.id)
	session.add(db_file)
	session.commit()
	session.refresh(db_file)
	return db_file


def delete_file(session: Session, file_id: int):
	file = get_file(session, file_id)
	session.delete(file)
	session.commit()
### PROTOCOL CRUD ###
def get_protocol(session: Session, protocol_id: int):
	return session.query(models.Protocol).filter_by(id=protocol_id).first()

def protocol_exists(session: Session, filename: str) -> bool:
	protocol =  session.query(models.Protocol).filter_by(filename=filename).first()
	return not not protocol
def get_protocols(session: Session):
	return session.query(models.Protocol).all()
def create_protocol(session: Session, protocol: schemas.ProtocolCreate):
	db_protocol = models.Protocol(**protocol.dict())
	session.add(db_protocol)
	session.commit()
	session.refresh(db_protocol)
	return db_protocol
def delete_protocol(session: Session, protocol_id: int):
	protocol = get_protocol(session, protocol_id)
	session.delete(protocol)
	session.commit()

