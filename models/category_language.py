from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base


class CategoryLanguage(Base):
    __tablename__ ='category_language'

    category_id = Column(Integer, ForeignKey("category.category_id"), primary_key=True)
    language_id = Column(Integer, ForeignKey("language.language_id"), primary_key=True)
    category_name = Column(String(100), nullable=False)

    categories = relationship("Category", back_populates="category_languages")
    languages = relationship("Language", back_populates="category_languages")