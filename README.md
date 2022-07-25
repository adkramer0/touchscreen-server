# touchscreen-server
web-interface for touchscreen project

--- 

# Setup Guide
- device/server config
	- open ports, etc.
- set web url or ip in /frontend/src/main.js
- set all env vars in docker-compose.yml and in /database/db.conf
- run.sh
- register first user
- sign in with creds: u: admin, p: admin
	- verify first user
- either sign in with new user and remove admin or run.sh (both get rid of admin once registered user)
- good to go!

---

# API

## TODO

- add protocol update endpoint
	- update file hash
	- devices compare current hash to hashes from db, if hash is different, download updated protocol and replace
- video streaming from pi to user
- longterm
	- switch all postgres stuff to mongo
	- add device flow for OAuth 2!!
	- refactor project structure
		- crud
		- schemas
		- dependencies
		- utils

---

# Frontend

## TODO
- add select all/none option to tables
- filter functions for tables
	- i.e., for device files, filter for sytem logs, select all, delete
---