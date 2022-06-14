from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from .. import dependencies, crud, schemas, utils
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
router = APIRouter(prefix='/users')

@router.get('/devices', response_model=list[schemas.Device])
async def get_devices(verified: bool, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	 return crud.get_devices(session, verified)

@router.get('/', response_model=list[schemas.User])
async def get_users(verified: bool, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	return crud.get_users(session, verified)


@router.post('/upload', response_model=list[schemas.Protocol])
async def upload_protocols(files: list[UploadFile], user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs)):
	files_created = []
	file_names = await utils.save_protocols(files)
	async for file in file_names:
		file_id = await fs.upload_from_stream(file.filename, file.file)
		protocols = await utils.extract_protocols(file)
		file_created = schemas.ProtocolCreate(filename=file, mongo_id=file_id, protocols=protocols)
		new_file = crud.create_protocol(session, file_created)
		file_created.append(new_file)
	return files_created



@router.get('/download/{mongo_id}', response_class=StreamingResponse)
async def download_file(mongo_id: str, str, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session), fs: AsyncIOMotorGridFSBucket = Depends(dependencies.get_fs)):
	grid_out = await fs.open_download_stream(mongo_id)
	return utils.chunk_generator(grid_out)


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
"""
@router.post('devices/run')
async def run_protocol(protocol: str, file: schemas.File, user: schemas.User = Depends(dependencies.user_authorized), session: Session = Depends(dependencies.get_session)):
	protocols = await utils.extract_protocols(file.local_path)
	if protocol in protocols:
		raise HTTPException(status_code=404, detail='protocol not found')
	return protocol
"""