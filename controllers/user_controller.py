from models.user import User
from config import db
from fastapi import HTTPException

collection =db.users

async def create_user(user:User):
    result = await collection.insert_one(user.dict(by_alias=True))
    return str(result.inserted_id)


async def get_all_users():
    users = []
    cursor = collection.find({})
    async for document in cursor:
        users.append(User(**document))
    return users

async def get_user_by_email(email: str):
    user = await collection.find_one({"email":email})
    if user:
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")
