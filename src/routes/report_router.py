from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import jwt_required
from src.config.configuration import get_db
from src.controllers.report_controller import ReportController

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/upload")
async def upload_reports(
    files: List[UploadFile] = File(...),
    user_payload: dict = Depends(jwt_required),
    db: AsyncSession = Depends(get_db),
):
    """Upload multiple report files (Protected endpoint)"""
    try:
        result = await ReportController.upload_reports(files, user_payload, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


@router.get("/my-reports")
async def get_my_reports(
    user_payload: dict = Depends(jwt_required), db: AsyncSession = Depends(get_db)
):
    """Get all reports for the authenticated user"""
    result = await ReportController.get_user_reports(user_payload, db)
    return result


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    user_payload: dict = Depends(jwt_required),
    db: AsyncSession = Depends(get_db),
):
    """Delete a specific report"""
    try:
        result = await ReportController.delete_report(report_id, user_payload, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting report: {str(e)}")
