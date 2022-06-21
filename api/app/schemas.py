from pydantic import BaseModel

class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str 
	email: str

class User(UserBase):
	id: int 
	verified: bool

	class Config:
		orm_mode = True
class UserID(BaseModel):
	id: int
	class Config:
		orm_mode = True

class FileBase(BaseModel):
	filename: str 
	content_id: str


class FileCreate(FileBase):
	pass 

class File(FileBase):
	id: int 
	device_id: int

	class Config:
		orm_mode = True


class DeviceBase(BaseModel):
	name: str

class DeviceCreate(DeviceBase):
	password: str 

class Device(DeviceBase):
	id: int 
	verified: bool
	status: str | None = None
	files: list[File] = []

	class Config:
		orm_mode = True

class DeviceNoFiles(DeviceBase):
	id: int
	verified: bool
	status: str | None = None

	class Config:
		orm_mode = True

class DeviceName(DeviceBase):
	id: int
	class Config:
		orm_mode = True
class DeviceID(BaseModel):
	id: int
	class Config:
		orm_mode = True
class ProtocolBase(BaseModel):
	filename: str
	content_id: str
	protocols: list[str]

class ProtocolCreate(ProtocolBase):
	pass 

class Protocol(ProtocolBase):
	id: int

	class Config:
		orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

