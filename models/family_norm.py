from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class FamilyNorm(Base):
    __tablename__ = 'family_norm'

    family_norm_id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)

    norm = relationship("Norm", back_populates="family_norm")
