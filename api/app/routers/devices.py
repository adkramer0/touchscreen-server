from fastapi import APIRouter, HTTPException, UploadFile, Depends, Request, WebSocket
from fastapi.websockets import WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
import werkzeug
import gridfs
from .. import dependencies, crud, schemas
from ..utils import utils, custom_response
from ..utils.ConnectionManager import device_manager
router = APIRouter(prefix='/devices')

@router.get('/whoami', response_model=schemas.DeviceID)
async def whoami(device: schemas.DeviceID = Depends(dependencies.device_authorized)):
	return device

@router.put('/status', response_model=schemas.Device)
async def set_status(status: str, device: schemas.DeviceID = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	device = crud.get_device(session, device)
	device.status = status
	session.commit()
	session.refresh(device)
	return device

@router.get('/download/{content_id}')
async def download_protocol(content_id: str, device: schemas.DeviceID = Depends(dependencies.device_authorized), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	content_id = ObjectId(content_id)
	try:
		grid_out = await fs.open_download_stream(content_id)
	except gridfs.NoFile:
		raise HTTPException(status_code=404, detail='Resource not found')
	return custom_response.AsyncIOMotorFileResponse(grid_out)

@router.post('/upload', response_model=list[schemas.File])
async def upload_files(files: list[UploadFile], device: schemas.DeviceID = Depends(dependencies.device_authorized), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	new_files = []
	for file in files:
		file.filename = werkzeug.utils.secure_filename(file.filename)
		file_id = await fs.upload_from_stream(file.filename, file.file)
		file_id = str(file_id)
		file_created = schemas.FileCreate(filename=file.filename, content_id=file_id)
		new_file = crud.create_file(session, file_created, device)
		new_files.append(new_file)
	return new_files

@router.get('/files', response_model=list[schemas.File])
async def get_files(device: schemas.DeviceID = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files = crud.get_files(session, device)
	return files

@router.get('/protocols', response_model=list[schemas.Protocol])
async def get_protocols(device: schemas.DeviceID = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files = crud.get_protocols(session)
	return files

@router.websocket('/stream')
async def websocket_devices(websocket: WebSocket, device_id: schemas.DeviceID = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	await device_manager.connect(websocket, device_id, session)
	device = crud.get_device(session, device_id)
	try:
		while True:
			data = await websocket.receive_json()
			device.status = data.get('status')
			session.commit()
			session.refresh(device)
	except WebSocketDisconnect:
		device_manager.disconnect(device_id, session)
