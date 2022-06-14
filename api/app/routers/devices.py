from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from .. import dependencies, crud, schemas, utils

router = APIRouter(prefix='/devices')

@router.put('/status', response_model=schemas.Device)
async def set_status(status: str, device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	device = crud.get_device(session, device.id)
	device.status = status
	session.commit()
	session.refresh(device)
	return device

@router.get('/download/{mongo_id}', response_class=StreamingResponse)
async def download_protocol(mongo_id: str, device: schemas.Device = Depends(dependencies.device_authorized), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	grid_out = await fs.open_download_stream(mongo_id)
	return utils.chunk_generator(grid_out)

@router.post('/upload', response_model=list[schemas.File])
async def upload_files(files: list[UploadFile], device: schemas.Device = Depends(dependencies.device_authorized), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs), session: Session = Depends(dependencies.get_session)):
	new_files = []
	async for file in files:
		file_id = await fs.upload_from_stream(file.filename, file.file)
		file_created = schemas.FileCreate(filename=file.filename, mongo_id=file_id)
		new_file = crud.create_file(session, file_created, device.id)
		new_files.append(new_file)
	return new_files

@router.get('/files', response_model=list[schemas.File])
async def get_files(device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files = crud.get_files(session, device.id)
	return files

@router.get('/protocols', response_model=list[schemas.Protocol])
async def get_protocols(device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files = crud.get_protocols(session)
	return files


@router.delete('/files/remove', response_model=list[schemas.File])
async def remove_files(files: list[schemas.File], device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	for file in files:
		crud.delete_file(session, file.id)
	return files