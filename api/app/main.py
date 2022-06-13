from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .routers import users, devices
from . import models
from .database import engine
from .schemas import Token
from .utils import authenticate_user, authenticate_device, create_access_token
from .dependencies import get_session
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(devices.router)

@app.post('/token', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
	client = form_data.scopes[0]
	login_exception = HTTPException(
        status_code=401,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
	if client == 'user':
		user = authenticate_user(session, form_data.username, form_data.password)
		if not user:
			raise login_exception
		access_token = create_access_token(data={'sub': client+':'+user.username})
	elif client == 'device':
		device = authenticate_device(session, form_data.username, form_data.password)
		if not device:
			raise login_exception
		access_token = create_access_token(data={'sub': client+':'+client.id})
	else:
		raise HTTPException(status_code=400, detail='client scope unrecognized')
	return {"access_token": access_token, "token_type": "bearer"}