from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from .. import dependencies, crud, schemas, utils

router = APIRouter(prefix='/users')

@router.get('/devices', response_model=list[schemas.Device])
async def get_devices(verified: bool, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	 return crud.get_devices(session, verified)

@router.get('/', response_model=list[schemas.User])
async def get_users(verified: bool, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	return crud.get_users(session, verified)

@router.post('/upload', response_model=list[schemas.File])
async def upload_files(files: list[UploadFile], devices: list[schemas.Device], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	all_files = []
	for device in devices:
		files_created = await utils.save_files(files, device.id)
		new_files = crud.create_files(session, files_created, device.id)
		all_files.extend(new_files)
	return all_files


@router.get('/download/{device_id}/{filename}', response_class=FileResponse)
async def download_file(device_id: int, filename: str, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	file = crud.get_file_by_name(session, filename, device_id)
	if file:
		return file.local_path
	raise HTTPException(status_code=404, detail='could not find file')


@router.put('/devices/verify', response_model=list[schemas.Device])
async def verify_devices(devices: list[schemas.Device], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	device_ids = [device.id for device in devices]
	verified_devices = crud.verify_devices(session, device_ids)
	return verified_devices


@router.put('/verify', response_model=list[schemas.User])
async def verify_users(users: list[schemas.User], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	user_ids = [unv_user.id for unv_user in users]
	verified_users = crud.verify_users(session, user_ids)
	return verified_users

@router.delete('/devices/remove', response_model=list[schemas.Device])
async def remove_devices(devices: list[schemas.Device], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	for device in devices:
		crud.delete_device(session, device.id)
	return devices

@router.delete('/remove', response_model=list[schemas.User])
async def remove_users(users: list[schemas.User], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	for c_user in users:
		crud.delete_user(sessioin, c_user.id) 
	return users

@router.get('/protocols')
async def get_protocols(file: schemas.File, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	protocols = await utils.extract_protocols(file.local_path)
	return protocols

@router.post('devices/run')
async def run_protocol(protocol: str, file: schemas.File, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	protocols = await utils.extract_protocols(file.local_path)
	if protocol in protocols:
		raise HTTPException(status_code=404, detail='protocol not found')
	return protocol