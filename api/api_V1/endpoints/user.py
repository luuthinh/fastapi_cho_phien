from fastapi import APIRouter, Body, Depends

from ....core.jwt import get_current_user_authorizer
from ....crud.shortcuts import check_free_username_and_email
from ....crud.user import update_user
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.user import User, UserInResponse, UserInUpdate

router = APIRouter()


@router.get("/user", response_model=UserInResponse, tags=["users"])
async def retrive_current_user(user: User = Depends(get_current_user_authorizer)):
    return UserInResponse(user=user)

