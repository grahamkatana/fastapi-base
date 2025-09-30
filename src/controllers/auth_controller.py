from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User
from src.utils.auth import create_access_token
import random


class AuthController:
    @staticmethod
    async def send_otp(phone_number: str, db: AsyncSession):
        """Send OTP to phone number"""
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Find or create user
        result = await db.execute(select(User).where(User.phone_number == phone_number))
        user = result.scalar_one_or_none()

        if not user:
            user = User(phone_number=phone_number)
            db.add(user)

        # Set OTP and expiry (10 minutes)
        user.otp = otp
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)

        await db.commit()
        await db.refresh(user)

        # TODO: Send OTP via SMS service
        print(f"OTP for {phone_number}: {otp}")

        return {"message": "OTP sent successfully"}

    @staticmethod
    async def verify_otp(phone_number: str, otp: str, db: AsyncSession):
        """Verify OTP and return JWT token"""
        result = await db.execute(select(User).where(User.phone_number == phone_number))
        user = result.scalar_one_or_none()

        if not user or user.otp != otp:
            return None

        if user.otp_expires_at < datetime.utcnow():
            return None

        # Clear OTP
        user.otp = None
        user.otp_expires_at = None
        await db.commit()

        # Generate JWT
        access_token = create_access_token(
            data={"sub": phone_number, "user_id": user.id}
        )

        return {"access_token": access_token, "token_type": "bearer"}
