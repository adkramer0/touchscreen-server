from pydantic import BaseModel

class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str 

class User(UserBase):
	id: int 
	verified: bool

	class Config:
		orm_mode = True

class DeviceBase(BaseModel):
	name: str

class DeviceCreate(DeviceBase):
	token: str 

class Device(DeviceBase):
	id: int 
	verified: bool
	status: str | None = None
	files: list[File] = []

	class Config:
		orm_mode = True


class FileBase(BaseModel):
	filename: str 
	extension: str



class FileCreate(FileBase):
	pass 

class File(FileBase):
	id: int 
	local_path: int 
	device_id: int

	class Config:
		orm_mode = True