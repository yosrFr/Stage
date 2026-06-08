from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import configure_mappers
from models.base import Base

engine = create_engine("sqlite:///test.db", echo=False)

try:
    # 1. Validate relationships
    configure_mappers()
    print("Relationships OK")

    # 2. Create schema
    Base.metadata.create_all(bind=engine)
    print("Schema created")

    # 3. Inspect DB
    inspector = inspect(engine)

    print("\nTables found:")
    for table in inspector.get_table_names():
        print(" -", table)

        for col in inspector.get_columns(table):
            print(f"    {col['name']} ({col['type']})")

except Exception as e:
    print("ERROR FOUND:")
    print(e)