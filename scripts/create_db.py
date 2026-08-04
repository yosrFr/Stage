from database.engine import engine
from models.base import Base
from models.report_config import ReportConfig
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
