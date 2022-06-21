# touchscreen-server
web-interface for touchscreen project

# Setup Guide

# API

## TODO
- on database create, get any protocols from github and add them
- email validation
- reset password functionality for users
	- on forgot password page
		- user enters username
		- generate reset token
		- user is routed to reset password page
		- email is sent to cooresponding user email containing reset token
		- user copys token from email to field for token, and enters new password
		- if token matches, reset password/destroy token
- for protocol updates
	- create file hash on upload and store in db.
	- on file update
		- update the file hash
	- when devices poll protocols, the download new ones like usual and remove ones that are gone
		- devices compare current hash to hashes from db, if hash is different, download new protocol and replace

# Frontend

