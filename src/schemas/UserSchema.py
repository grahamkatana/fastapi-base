from pydantic import BaseModel
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    phone_number: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
