from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.db.database import get_db
from src.controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])


class SendOTPRequest(BaseModel):
    phone_number: str


class VerifyOTPRequest(BaseModel):
    phone_number: str
    otp: str


@router.post("/send-otp")
async def send_otp(request: SendOTPRequest, db: AsyncSession = Depends(get_db)):
    """Send OTP to phone number"""
    result = await AuthController.send_otp(request.phone_number, db)
    return result


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP and get JWT token"""
    result = await AuthController.verify_otp(request.phone_number, request.otp, db)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    return result
