from database.engine import engine
from models.base import Base
import models

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")