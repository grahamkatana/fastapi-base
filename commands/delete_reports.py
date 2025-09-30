import os
import asyncio
from sqlalchemy import select, delete
from src.config.configuration import get_settings
from src.db.database import AsyncSessionLocal
from src.models.report import Report


async def delete_reports_from_storage():
    """Delete all reports from storage directory and database"""
    settings = get_settings()
    storage_path = settings.STORAGE_PATH

    async with AsyncSessionLocal() as db:
        # Get all reports from database
        result = await db.execute(select(Report))
        reports = result.scalars().all()

        deleted_count = 0

        # Delete files from storage
        for report in reports:
            if os.path.exists(report.file_path):
                try:
                    os.unlink(report.file_path)
                    print(f"Deleted file: {report.stored_filename}")
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {report.stored_filename}: {e}")

        # Delete all records from database
        await db.execute(delete(Report))
        await db.commit()

        print(f"\nTotal files deleted: {deleted_count}")
        print(f"All report records removed from database")


def main():
    """Entry point for the command"""
    asyncio.run(delete_reports_from_storage())


if __name__ == "__main__":
    main()
