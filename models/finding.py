from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.base import Base


class Finding(Base):
    """
    Mesures correctives et préventives
    Finding Table - Corrective and preventive findings
    PRIMARY KEY: finding_id
    """
    __tablename__ = "findings"

    finding_id = Column(Integer, primary_key=True, index=True)
    finding_text = Column(String(500), nullable=False, unique=True)
    show_as_suggestion = Column(Boolean, default=True, nullable=False)

    # Many-to-Many: Finding <-> QuestionResponse via ResponseFinding
    response_findings = relationship("ResponseFinding", back_populates="finding", cascade="all, delete-orphan")
