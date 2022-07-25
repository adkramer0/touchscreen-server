from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
import os
import shutil
import pyclbr
import svn.remote
import werkzeug
import hashlib

from ..data import database, models
from .. import crud, schemas, dependencies

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


async def extract_protocols(filename: str, no_tmp: bool = False):
	file = 'tmp_' + filename.split('.', 1)[0] if not no_tmp else filename.rsplit('.', 1)[0] # get files name without path, and without extension
	module = pyclbr.readmodule(file) # load info on all classes in file
	protocols = []
	for k, v in module.items(): # check if base class is Protocol in all classes
		for base in v.super:
			if base == 'Protocol':
				protocols.append(k)
	return protocols

async def file_hash(file):
	file.seek(0)
	fhash = hashlib.md5(file.read()).hexdigest()
	file.seek(0)
	return fhash
async def init_db():
	models.Base.metadata.create_all(bind=database.engine)
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
	if len(crud.get_protocols(session)) == 0:
		# get datastore
		fs = await dependencies.get_fs()
		# use svn to get the protocols folder from the main branch
		r = svn.remote.RemoteClient('https://github.com/moormanlab/touchscreen/trunk/protocols')
		r.export(os.path.join(os.getcwd(), 'protocols'))
		for filename in os.listdir('protocols'):
			fname = werkzeug.utils.secure_filename(filename)
			path = os.path.join('protocols', fname)
			# read protocol and save it to gridfs bucket
			with open(os.path.join('protocols', filename), 'rb') as f:
				file_id = await fs.upload_from_stream(fname, f.read())
				f.seek(0)
				fhash = await file_hash(f)
			file_id = str(file_id)
			protocols = await extract_protocols('protocols.'+filename, no_tmp=True)
			file_created = schemas.ProtocolCreate(filename=fname, content_id=file_id, protocols=protocols, hash=fhash)
			new_file = crud.create_protocol(session, file_created)
		shutil.rmtree(os.path.join(os.getcwd(), 'protocols'))

	session.close()

