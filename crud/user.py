from ..db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from bson.objectid import ObjectId

from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate


async def get_user(conn: AsyncIOMotorClient, username: str) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"username": username})
    if row:
        return UserInDB(**row)


async def get_user_by_email(conn: AsyncIOMotorClient, email: EmailStr) -> UserInDB:
    row = await conn[database_name][users_collection_name].find_one({"email": email})
    if row:
        return UserInDB(**row)


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    db_user = UserInDB(**user.dict())
    db_user.change_password(user.password)

    row = await conn[database_name][users_collection_name].insert_one(db_user.dict())

    db_user.id = row.inserted_id
    db_user.created_at = ObjectId(db_user.id).generation_time
    db_user.updated_at = ObjectId(db_user.id).generation_time

    return db_user


async def update_user(conn: AsyncIOMotorClient, username:str, user: UserInUpdate) -> UserInDB:
    db_user = await get_user(conn, username)

    db_user.username = user.username or db_user.username
    db_user.email = user.email or db_user.email
    db_user.bio = user.bio or db_user.bio
    db_user.image = user.image or db_user.image
    if user.password:
        db_user.change_password(user.password)
    
    updated_at = await conn[database_name][users_collection_name].update_one({"username": db_user.username}, {'$set': db_user.dict()})
    db_user.updated_at = updated_at
    return db_user
