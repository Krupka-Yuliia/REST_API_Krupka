import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://mongo_admin:password@localhost:27017")
db = client.books
