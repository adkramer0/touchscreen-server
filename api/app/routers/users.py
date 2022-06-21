from fastapi import APIRouter, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson.objectid import ObjectId
import werkzeug
import gridfs
from .. import dependencies, crud, schemas
from ..utils import utils, custom_response

router = APIRouter(prefix='/users', dependencies=[Depends(dependencies.user_authorized)])

@router.get('/whoami', response_model=schemas.User)
async def whoami(user: schemas.User = Depends(dependencies.user_authorized)):
	return user

@router.get('/devices', response_model=list[schemas.Device])
async def get_devices(verified: bool, session: Session = Depends(dependencies.get_session)):
	 return crud.get_devices(session, verified)

@router.get('/', response_model=list[schemas.User])
async def get_users(verified: bool, session: Session = Depends(dependencies.get_session)):
	return crud.get_users(session, verified)


@router.post('/upload', response_model=list[schemas.Protocol])
async def upload_protocols(files: list[UploadFile], session: Session = Depends(dependencies.get_session), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs)):
	files_created = []
	for file in files:
		file.filename = werkzeug.utils.secure_filename(file.filename)
	await utils.save_protocols(files)
	for file in files:
		file_id = await fs.upload_from_stream(file.filename, file.file)
		file_id = str(file_id)
		protocols = await utils.extract_protocols(file.filename)
		file_created = schemas.ProtocolCreate(filename=file.filename, content_id=file_id, protocols=protocols)
		new_file = crud.create_protocol(session, file_created)
		files_created.append(new_file)
	await utils.delete_protocols(files)
	return files_created



@router.get('/download/{content_id}')
async def download_file(content_id: str, session: Session = Depends(dependencies.get_session), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs)):
	content_id = ObjectId(content_id)
	try:
		grid_out = await fs.open_download_stream(content_id)
	except gridfs.NoFile:
		raise HTTPException(status_code=404, detail='Resource not found')
	return custom_response.AsyncIOMotorFileResponse(grid_out)

@router.put('/name/device', response_model=schemas.DeviceNoFiles)
async def name_device(device: schemas.DeviceName, session: Session = Depends(dependencies.get_session)):
	device = crud.set_device_name(session, **device.dict())
	return device
	
@router.put('/verify/devices', response_model=list[schemas.DeviceNoFiles])
async def verify_devices(devices: list[schemas.DeviceID], session: Session = Depends(dependencies.get_session)):
	verified_devices = crud.verify_devices(session, devices)
	return verified_devices


@router.put('/verify', response_model=list[schemas.User])
async def verify_users(users: list[schemas.UserID], session: Session = Depends(dependencies.get_session)):
	verified_users = crud.verify_users(session, users)
	return verified_users

@router.delete('/remove/devices')
async def remove_devices(devices: list[schemas.DeviceID], fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	for device in devices:
		files = crud.get_files(session, device)
		for file in files:
			content_id = ObjectId(file.content_id)
			await fs.delete(content_id)
		crud.delete_device(session, device)
	return

@router.delete('/remove')
async def remove_users(users: list[schemas.UserID], session: Session = Depends(dependencies.get_session)):
	for user in users:
		crud.delete_user(session, user) 
	return

@router.delete('/remove/files')
async def remove_files(files: list[schemas.File], fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	for file in files:
		crud.delete_file(session, file.id)
		content_id = ObjectId(file.content_id)
		await fs.delete(content_id)
	return

@router.delete('/remove/protocols')
async def remove_protocols(protocols: list[schemas.Protocol], fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	for protocol in protocols:
		crud.delete_protocol(session, protocol.id)
		content_id = ObjectId(protocol.content_id)
		await fs.delete(content_id)
	return

@router.get('/protocols', response_model=list[schemas.Protocol])
async def get_protocols(session: Session = Depends(dependencies.get_session)):
	protocols = crud.get_protocols(session)
	return protocols
"""
@router.post('devices/run')
async def run_protocol(protocol: str, file: schemas.File, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	protocols = await utils.extract_protocols(file.local_path)
	if protocol in protocols:
		raise HTTPException(status_code=404, detail='protocol not found')
	return protocol
"""