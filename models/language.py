from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Language(Base):
    __tablename__ ='language'

    language_id = Column(Integer, primary_key=True)
    language = Column(String(50))
    
    control_tag_languages = relationship("ControlTagLanguage", back_populates="languages")
    chapter_languages = relationship("ChapterLanguage", back_populates="languages")
    category_languages = relationship("CategoryLanguage", back_populates="languages")
    control_languages = relationship("ControlLanguage", back_populates="languages")