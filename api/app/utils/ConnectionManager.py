from fastapi import WebSocket
from sqlalchemy.orm import Session
from .. import schemas, crud

class ConnectionManager:
	def __init__(self):
		self.active_connections: dict[int, WebSocket] = {}
	
	async def connect(self, websocket: WebSocket, device: schemas.DeviceID, session: Session):
		await websocket.accept()
		self.active_connections.update({device.id: websocket})
		device = crud.get_device(session, device)
		device.online = True		
		session.commit()
		session.refresh(device)

	def disconnect(self, device: schemas.DeviceID, session: Session):
		websocket = self.active_connections.get(device.id)
		self.active_connections.pop(device.id)
		device = crud.get_device(session, device)
		device.online = False
		session.commit()
		session.refresh(device)

	async def send_message(self, data: dict, device: schemas.DeviceName):
		data.update({'subject': device.name})
		ws = self.active_connections.get(device.id)
		await ws.send_json(data)

	async def broadcast(self, event: str, data: dict, devices: list[schemas.DeviceName]):
		data.update({'event': event})
		for device in devices:
			await self.send_message(data, device)


device_manager = ConnectionManager()