import sys
from pathlib import Path

from dotenv import load_dotenv

# Ensure root and app are on sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
app_dir = Path(__file__).resolve().parent.parent
for p in [str(root_dir), str(app_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

load_dotenv()

try:
    from app.models.dbmodel import Job  # noqa: F401
    from app.workers.database import Base, engine
except ImportError:
    from workers.database import Base, engine


def init_db():
    try:
        Base.metadata.create_all(engine)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise


if __name__ == "__main__":
    init_db()
