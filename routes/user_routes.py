from fastapi import APIRouter, HTTPException
from app.models import User
from app.database import users_db

router = APIRouter()

@router.get("/")
def get_all_users():
    return users_db

@router.post("/")
def create_user(user: User):
    if any(u.id == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="User ID already exists")
    users_db.append(user)
    return user

@router.get("/{user_id}")
def get_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(user_id: int, updated_user: User):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": "User deleted successfully"}

@router.post("/{user_id}/deactivate")
def deactivate_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    return {"message": "User deactivated"}

