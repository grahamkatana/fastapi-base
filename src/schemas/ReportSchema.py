from pydantic import BaseModel
from datetime import datetime
from typing import Optional


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
