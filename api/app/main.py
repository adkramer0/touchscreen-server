from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .routers import users, devices
from . import crud, dependencies, schemas
from .utils import utils
from .data import models, datastore, database

app = FastAPI(root_path='/api')

app.include_router(users.router)
app.include_router(devices.router)

app.add_event_handler('startup', datastore.connect)
app.add_event_handler('shutdown', datastore.disconnect)

models.Base.metadata.create_all(bind=database.engine)
utils.init_db()


@app.post('/token', response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(dependencies.get_session)):
	try:
		client = form_data.scopes[0]
	except IndexError:
		client = 'user' # temporary for testing with docs
	login_exception = HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
	if client == 'user':
		user = await utils.authenticate_user(session, form_data.username, form_data.password)
		if not user:
			raise login_exception
		access_token = utils.create_access_token(data={'sub': client+':'+user.username})
	elif client == 'device':
		device = await utils.authenticate_device(session, schemas.DeviceID(id=int(form_data.username)), form_data.password)
		if not device:
			raise login_exception
		access_token = utils.create_access_token(data={'sub': client+':'+str(device.id)})
	else:
		raise HTTPException(status_code=400, detail='client scope unrecognized')
	return {"access_token": access_token, "token_type": "bearer"}

@app.post('/users/register', response_model=schemas.User)
def register_user(user: schemas.UserCreate, session: Session = Depends(dependencies.get_session)):
	if user.username == 'admin':
		raise HTTPException(status_code=409, detail='admin username reserved')
	try:
		new_user = crud.create_user(session, user)
	except IntegrityError:
		raise HTTPException(status_code=409, detail='username already taken')
	return new_user

@app.post('/devices/register', response_model=schemas.DeviceNoFiles)
def register_device(device: schemas.DeviceCreate, session: Session = Depends(dependencies.get_session)):
	try:
		new_device = crud.create_device(session, device)
	except IntegrityError:
		raise HTTPException(status_code=409, detail='name already taken')
	return new_device