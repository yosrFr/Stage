from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class QuestionResponse(Base):
    """
    QuestionResponse Table - Responses to control questions during audits
    PRIMARY KEY: response_id
    """
    __tablename__ = "question_responses"

    response_id = Column(Integer, primary_key=True, index=True)
    control_id = Column(Integer, ForeignKey("control.control_id"), nullable=False)

    risk_level = Column(Integer)
    current_state = Column(String(5000))
    non_conformity = Column(String(50))

    # Relations Many-to-One
    control = relationship("Control", back_populates="question_responses")
    measures = relationship("Measure", back_populates="response")

    # Many-to-Many: QuestionResponse <-> Finding via ResponseFinding
    response_findings = relationship("ResponseFinding", back_populates="question_response",
                                     cascade="all, delete-orphan")
