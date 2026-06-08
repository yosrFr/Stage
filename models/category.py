from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Category(Base):
    __tablename__ ='category'

    category_id = Column(Integer, primary_key=True)
    id = Column(String, nullable=False)
    norm_id = Column(Integer, ForeignKey('norms.norm_id'), nullable=False)

    norms = relationship("Norm", back_populates="category")
    category_languages = relationship("CategoryLanguage", back_populates="categories")
    controls = relationship("Control", back_populates="categories")