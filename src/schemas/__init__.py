from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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


# Report Schemas
class ReportBase(BaseModel):
    original_filename: str


class ReportResponse(ReportBase):
    id: int
    stored_filename: str
    file_size: Optional[int]
    mime_type: Optional[str]
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    count: int
    reports: list[ReportResponse]
