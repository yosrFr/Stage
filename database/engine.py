from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:0000@localhost:5432/stage"

engine = create_engine(DATABASE_URL, echo=True)
