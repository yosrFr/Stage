from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from sqlalchemy import UniqueConstraint


class Measure(Base):
    """
    Mesures correctives et préventives
    Measure Table - Corrective and preventive measure
    PRIMARY KEY: measure_id
    """
    __tablename__ = "measure"

    measure_id = Column(Integer, primary_key=True, index=True)
    measure_text = Column(String(1000), nullable=False)
    response_id = Column(Integer, ForeignKey("question_responses.response_id"), nullable=False)

    response = relationship("QuestionResponse", back_populates="measures")

    # unique constraint
    __table_args__ = (
        UniqueConstraint('measure_text', 'response_id', name='measure_text_response_unique'),
    )