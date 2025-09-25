from fastapi import APIRouter
from models.user import User
from controllers import user_controller

router = APIRouter(prefix="/users", tags=["users"])


@router.post('/create_user')
async def create_user(user: User):
    try:
        return await user_controller.create_user(user)
    except Exception as e:
        return {"error": str(e)}
@router.get('/')
async def get_all_users():
    try:
        return await user_controller.get_all_users()
    except Exception as e:
        return {"error": str(e)}
    
@router.get('/{email}')
async def get_user_by_email(email: str):
    try:
        return await user_controller.get_user_by_email(email)
    except Exception as e:
        return {"error": str(e)}