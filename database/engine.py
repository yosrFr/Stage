from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/auditaas"


engine = create_engine(DATABASE_URL)

Base = declarative_base()