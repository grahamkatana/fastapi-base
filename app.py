from fastapi import FastAPI
from src.routes import auth_router, report_router
from src.db.database import engine, Base

app = FastAPI(title="FastAPI Application")

# Include routers
app.include_router(auth_router.router)
app.include_router(report_router.router)


@app.on_event("startup")
async def startup():
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Application"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
