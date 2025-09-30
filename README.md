# Run migrations (first time)

uv run alembic revision --autogenerate -m "Initial migration"
uv run alembic upgrade head

# Run the application

uv run uvicorn app:app --reload

# Run the delete command

uv run python commands/delete_reports.py
