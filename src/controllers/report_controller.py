from fastapi import UploadFile
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid
import aiofiles
from src.config.configuration import get_settings
from src.models.report import Report
from src.models.user import User

settings = get_settings()


class ReportController:
    @staticmethod
    async def upload_reports(
        files: List[UploadFile], user_payload: dict, db: AsyncSession
    ):
        """Upload multiple report files and save to database"""
        # Create storage directory if it doesn't exist
        os.makedirs(settings.STORAGE_PATH, exist_ok=True)

        # Get user from database
        user_id = user_payload.get("user_id")
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        saved_files = []

        for file in files:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.STORAGE_PATH, unique_filename)

            # Save file asynchronously
            async with aiofiles.open(file_path, "wb") as f:
                content = await file.read()
                await f.write(content)

            # Get file size
            file_size = os.path.getsize(file_path)

            # Create report record in database
            report = Report(
                user_id=user.id,
                original_filename=file.filename,
                stored_filename=unique_filename,
                file_path=file_path,
                file_size=file_size,
                mime_type=file.content_type,
            )
            db.add(report)

            saved_files.append(
                {
                    "id": None,  # Will be populated after commit
                    "original_name": file.filename,
                    "saved_name": unique_filename,
                    "file_size": file_size,
                    "mime_type": file.content_type,
                }
            )

        await db.commit()

        # Refresh to get IDs
        for i, file_info in enumerate(saved_files):
            result = await db.execute(
                select(Report).where(Report.stored_filename == file_info["saved_name"])
            )
            report = result.scalar_one()
            file_info["id"] = report.id

        return {
            "message": "Reports uploaded successfully",
            "count": len(saved_files),
            "files": saved_files,
        }

    @staticmethod
    async def get_user_reports(user_payload: dict, db: AsyncSession):
        """Get all reports for a user"""
        user_id = user_payload.get("user_id")

        result = await db.execute(
            select(Report)
            .where(Report.user_id == user_id)
            .order_by(Report.created_at.desc())
        )
        reports = result.scalars().all()

        return {
            "count": len(reports),
            "reports": [
                {
                    "id": report.id,
                    "original_filename": report.original_filename,
                    "stored_filename": report.stored_filename,
                    "file_size": report.file_size,
                    "mime_type": report.mime_type,
                    "created_at": report.created_at.isoformat(),
                }
                for report in reports
            ],
        }

    @staticmethod
    async def delete_report(report_id: int, user_payload: dict, db: AsyncSession):
        """Delete a specific report"""
        user_id = user_payload.get("user_id")

        result = await db.execute(
            select(Report).where(Report.id == report_id, Report.user_id == user_id)
        )
        report = result.scalar_one_or_none()

        if not report:
            raise ValueError("Report not found or unauthorized")

        # Delete file from storage
        if os.path.exists(report.file_path):
            os.remove(report.file_path)

        # Delete from database
        await db.delete(report)
        await db.commit()

        return {"message": "Report deleted successfully"}
