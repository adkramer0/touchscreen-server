from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from .. import dependencies, crud, schemas, utils

router = APIRouter(prefix='/devices')

@router.put('/status', response_model=schemas.Device)
async def set_status(status: str, device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	device = crud.get_device(session, device.id)
	device.status = status
	session.commit()
	session.refresh(device)
	return device

@router.get('/download/{filename}', response_class=FileResponse)
async def download_file(filename: str, device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	file = crud.get_file_by_name(session, filename, device.id)
	if file:
		return file.local_path
	raise HTTPException(status_code=404, detail='could not find file')

@router.post('/files/upload', response_model=list[schemas.File])
async def upload_files(files: list[UploadFile], device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files_created = await utils.save_files(files, device.id)
	new_files = crud.create_files(session, files_created, device.id)
	return new_files

@router.get('/files', response_model=list[schemas.File])
async def get_files(device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	files = crud.get_files(session, device.id)
	return files


@router.delete('/files/remove', response_model=list[schemas.File])
async def remove_files(files: list[schemas.File], device: schemas.Device = Depends(dependencies.device_authorized), session: Session = Depends(dependencies.get_session)):
	for file in files:
		crud.delete_file(session, file.id)
	return files