from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.models.users import UserCreate, UserUpdate


router = APIRouter(
    tags=['public']
)

@router.get("")
async def get_users(request: Request):
    users = []
    users_list = await request.app.mongodb['users'].find().to_list(length=100)
    for doc in users_list:
        users.append(doc)
    return users

@router.get("/{user_id}")
async def get_single_user(user_id: str, request: Request):
    if (user := await request.app.mongodb['users'].find_one({'_id': user_id})) is not None:
        return user
    
    raise HTTPException(status_code=404, detail=f"User {user_id} is not found")

@router.post("")
async def create_user(request: Request, user: UserCreate = Body(...)):
    json_user = jsonable_encoder(user)
    new_user = await request.app.mongodb['users'].insert_one(json_user)
    created_user = await request.app.mongodb['users'].find_one(
        {'id': new_user.id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

@router.put("/{user_id}")
async def update_user(user_id: str, request: Request, new_user: UserUpdate = Body(...)):
    user = {k: v for k, v in new_user.model_dump().items() if v is not None}

    if len(user) >= 1:
        update_result = await request.app.mongodb["users"].update_one(
            {"_id": user_id}, {"$set": user}
        )
        if update_result.modified_count == 1:
            if (
                updated_user := await request.app.mongodb["users"].find_one(
                    {"id": user_id}
                )
            ) is not None:
                return updated_user
    
    if (
        existing_task := await request.app.mongodb["users"].find_one(
                    {"id": user_id}
                )
    ) is not None:
        return existing_task
    
    raise HTTPException(status_code=404, detail=f"User {user_id} is not found")

@router.delete("/{user_id}")
async def delete_user(request: Request, user_id: str):
    delete_result = await request.app.mongodb['users'].delete_one(user_id)
    
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {user_id} is not found")
