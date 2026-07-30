import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mydb")
engine = create_engine(DATABASE_URL)