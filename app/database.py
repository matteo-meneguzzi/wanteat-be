import os
import motor


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])
db = client.get_database("wanteat")
restaurant_collection = db.get_collection("restaurants")
user_collection = db.get_collection("users")