from fastapi import FastAPI
from .routers import users, devices
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(devices.router)