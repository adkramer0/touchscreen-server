# touchscreen-server
web-interface for touchscreen project

# TODO

- [ ] /api/Dockerfile
- [x] /api/app/main.py
	- POST: /users/register
		- request: UserCreate
		- response_model: User
	- POST: /devices/register
		- request: DeviceCreate
		- response_model: Device

- [x] /api/app/routers/users.py
	- GET: /devices
		- parameter: (bool) verified
		- response_model: list(Device)
	- GET: /users
		- parameter: (bool) verified
		- response_model: list(User)
	- POST: /upload
		- request: list(Device)
		- Files
		- response_model: File
	- GET: /download/{device_id}/{extension}/{filename}
		- response_class: FileResponse
	- PUT: /devices/verify
		- request: list(Device)
		- response_model: list(Device)
	- PUT: /users/verify
		- request: list(User)
		- response_model: list(User)
	- DELETE: /users/remove
		- request: list(User)
		- response_model: list(User)
	- DELETE: /devices/remove
		- request: list(Device)
		- response_model: list(Device)
	- GET: /devices/protocols:
		- request: Device
		- response_model: list(Protocol)
	- POST: /devices/run: 
		- request: Protocol, Device
		- response_model: Protocol

- [x] /api/app/routers/devices.py
	- PUT: /status
		- request: Device
		- response_model: Device
	- GET: /download/{device_id}/{extension}/{filename}
		- response_class: FileResponse
	- POST: /files/upload
		- Files
		- response_model: list(File)
	- GET: /files
		- response_model: list(File)
	- DELETE: /files/remove
		- request: list(File)
		- respnse_model: list(File)
	- socket: /new_protocol (data: extension, filename)
	- socket: /run_protocol (data: filename, protocol_name, device_name, user_username)

- [x] /database/db.conf
- [ ] /frontend/*
- [ ] /nginx/nginx.conf

