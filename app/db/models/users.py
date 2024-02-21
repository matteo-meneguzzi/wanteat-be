import uuid
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from app.db.models.permissions import PermissionEnum

class RestaurantBase(BaseModel):
    pass

class UserBase(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias = "_id")
    name: Optional[str] = None
    surname: Optional[str] = None
    age: Optional[int] = None
    username: str = Field(...)
    email: EmailStr = Field(...)
    permissions: List[PermissionEnum]
    
    @validator('permissions')
    def validate_permissions(cls, v):
        if set(v) != {PermissionEnum.READ_RESTAURANTS, PermissionEnum.WRITE_RESTAURANTS}:
            raise ValueError("Base user permissions must be READ and WRITE only")
        return v

class UserCreate(UserBase):
    password: str = Field(...)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    hashed_password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Owner(UserBase):
    permissions: List[PermissionEnum]
    is_owner: bool = False
    restaurants: List[RestaurantBase]
    
    @validator('permissions')
    def validate_permissions(cls, v):
        if set(v) != {PermissionEnum.READ_RESTAURANTS, PermissionEnum.WRITE_RESTAURANTS, PermissionEnum.DELETE_RESTAURANTS}:
            raise ValueError("Owner user permissions must be READ, WRITE and DELETE only")
        return v
    
class OwnerUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    restaurants: List[RestaurantBase]
    
class Admin(UserBase):
    permissions: List[PermissionEnum]
    
