from motor.motor_asyncio import AsyncIOMotorClient
import os

class Datastore:
    client: AsyncIOMotorClient = None

db = Datastore()

async def get_gridfs():
	return db.client.gridfs

async def connect():
	db.client = AsyncIOMotorClient(os.environ.get('MONGO_DATABASE_HOST'))
async def disconnect():
	db.client.close()