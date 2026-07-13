from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class ResponseFinding(Base):
    """
    ResponseFinding Table - Junction table for QuestionResponse and Finding
    COMPOSITE PRIMARY KEY: (response_id, finding_id)
    """
    __tablename__ = "response_findings"

    response_id = Column(Integer, ForeignKey("question_responses.response_id"), primary_key=True)
    finding_id = Column(Integer, ForeignKey("findings.finding_id"), primary_key=True)

    # Relationships

    # To the associated response: Many-to-One (each row links to a single response)
    question_response = relationship("QuestionResponse", back_populates="response_findings")

    # To the associated finding: Many-to-One (each row links to a single finding)
    finding = relationship("Finding", back_populates="response_findings")
