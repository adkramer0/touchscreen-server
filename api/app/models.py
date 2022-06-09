from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	password = Column(String)
	verified = Column(Boolean, default=False)

	def __init__(self, username: str, password: str, verified: bool = False):
		self.username = username
		self.password = pwd_context.hash(password)
		self.verified = verified

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)
	
class Device(Base):
	__tablename__ = 'devices'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)
	password = Column(String)
	verified = Column(Boolean, default=False, index=True)
	status = Column(String, index=True)

	files = relationship('File', back_populates='device')

	def __init__(self, name: str, password: str, verified: bool = False):
		self.name = name
		self.password = pwd_context.hash(password)
		self.verified = verified
		
	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

class File(Base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True, index=True)
	filename = Column(String, index=True) # of form "filename.csv"
	extension = Column(String, index=True) # of form "csv"
	local_path = Column(String, unique=True) # of form /{device_id}/{extension}/{filename}
	device_id = Column(Integer, ForeignKey('devices.id'))

	device = relationship('Device', back_populates='files')