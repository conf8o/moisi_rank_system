import os

DATABASE_URL = os.environ.get("MOISI_MATCHING_SYSTEM_DATABASE_URL", "postgresql://localhost:5432?user=app&password=password")
