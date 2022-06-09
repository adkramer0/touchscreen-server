from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	password = Column(String)
	verified = Column(Boolean, default=False)
	
class Device(Base):
	__tablename__ = 'devices'
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, unique=True, index=True)
	token = Column(String)
	verified = Column(Boolean, default=False, index=True)
	status = Column(String, index=True)

	files = relationship('File', back_populates='device')

class File(Base):
	__tablename__ = 'files'
	id = Column(Integer, primary_key=True, index=True)
	filename = Column(String, index=True) # of form "filename.csv"
	extension = Column(String, index=True) # of form "csv"
	local_path = Column(String, unique=True) # of form /{device_id}/{extension}/{filename}
	device_id = Column(Integer, ForeignKey('devices.id'))

	device = relationship('Device', back_populates='files')