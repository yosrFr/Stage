from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Norm(Base):
    __tablename__ = 'norms'

    norm_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, unique=True)
    abbreviation = Column(String(100), nullable=False)
    description = Column(String(1000))
    publish_year = Column(Integer, nullable=False)
    family_norm_id = Column(Integer, ForeignKey("family_norm.family_norm_id"), nullable=False)

    category = relationship("Category", back_populates="norms")
    chapters = relationship("Chapter", back_populates="norm")
    controls = relationship("Control", back_populates="norms")
    family_norm = relationship("FamilyNorm", back_populates="norm")
