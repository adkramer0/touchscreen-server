# touchscreen-server
web-interface for touchscreen project

--- 

# Setup Guide
- device/server congig
	- open ports, etc.
- set web url or ip in /frontend/src/main.js
- run.sh
- register first user
- sign in with creds: u: admin, p: admin
	- verify first user
- either sign in with new user and remove admin or run.sh (both get rid of admin once registered user)
- good to go!

---

# API

## TODO
- on database create, get any protocols from github and add them!!!!!
- reset password functionality for users
	- on forgot password page
		- user enters username
		- generate reset token
		- user is routed to reset password page
		- email is sent to cooresponding user email containing reset token (twilio send grid free plan?)
		- user copys token from email to field for token, and enters new password
		- if token matches, reset password/destroy token
- make protocol filenames unique in db?
- for protocol updates
	- create file hash on upload and store in db.
	- on file update
		- update the file hash
	- when devices poll protocols, the download new ones like usual and remove ones that are gone
		- devices compare current hash to hashes from db, if hash is different, download new protocol and replace
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
- handle axios errors
- display accurate status (i.e. running "protocol", updating) to active device list...
	- prevent new tasks from being added while running protocols

---